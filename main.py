import os
import shutil
import uuid
import asyncio
from typing import Dict
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from orchestrator import handle_next_step
from agents.resume_analyzer_agent import resume_analyzer_agent
from services.resume_ingestion import (
    load_documents, 
    get_chroma_vector_store, 
    get_pipeline, 
    get_index
)
from mcp_client import get_mcp_client
from states.interview_state import InterviewState

# Lifecycle management for MCP client to avoid anyio cancel scope issues
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MCP
    print("Connecting to MCP server...")
    client = get_mcp_client()
    try:
        await client.connect()
        print("MCP client connected.")
        yield
    finally:
        # Shutdown: Close MCP
        print("Closing MCP connection...")
        await client.close()

app = FastAPI(title="Agent Screening API", lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions: Dict[str, InterviewState] = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

def init_state() -> InterviewState:
    return {
        "resume_text": "",
        "skills": [],
        "projects": [],
        "question_list": [],
        "current_question": None,
        "candidate_answer": None,
        "score": None,
        "feedback": None,
        "evaluation": None,
        "conversation_history": [],
        "question_index": 0,
        "interview_complete": False,
        "final_report": None,
        "last_action": None
    }

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    session_id = str(uuid.uuid4())
    
    # 1. Save file locally
    upload_dir = "datas/resumes"
    os.makedirs(upload_dir, exist_ok=True)
    # Clear directory to ensure we only analyze ONE resume at a time for this session
    # (Simple approach for local prototype)
    for existing_file in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, existing_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception:
            pass

    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        print(f"Ingesting resume: {file.filename}")
        # 2. Ingest into Vector Store
        documents = load_documents(upload_dir)
        vector_store = get_chroma_vector_store("vector_store")
        pipeline = get_pipeline(vector_store)
        pipeline.run(documents=documents)
        
        # 3. Analyze Resume using LLM Agent
        print("Analyzing resume with LLM Agent...")
        full_text = "\n".join([doc.text for doc in documents])
        analysis = await resume_analyzer_agent(full_text)
        
        state = init_state()
        state["resume_text"] = full_text
        state["skills"] = analysis.get("skills", [])
        state["projects"] = analysis.get("projects", [])
        
        print(f"Extracted Skills: {state['skills']}")
        print(f"Extracted Projects: {state['projects']}")

        # 4. Get First Question
        state, msg_type, content = await handle_next_step(state)
        
        sessions[session_id] = state
        
        return {
            "session_id": session_id,
            "type": msg_type,
            "message": content,
            "skills": state["skills"],
            "projects": state["projects"]
        }
    except Exception as e:
        print(f"Error during upload/analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = sessions[session_id]
    
    if state.get("interview_complete"):
        return {
            "session_id": session_id,
            "type": "report",
            "message": state.get("final_report")
        }

    # Process next step
    state, msg_type, content = await handle_next_step(state, user_answer=request.message)
    
    sessions[session_id] = state
    
    return {
        "session_id": session_id,
        "type": msg_type,
        "message": content
    }

# Serve static files
os.makedirs("static", exist_ok=True)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
