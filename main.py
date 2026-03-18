import os
import shutil
import uuid
from typing import Dict
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from orchestrator import handle_next_step
from nodes.resume_analyzer_node import resume_analyzer_node
from mcp_client import get_mcp_client
from states.interview_state import InterviewState

app = FastAPI(title="Technical Interview Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for interview states (local development)
# In production, use Redis or a database
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
    
    # Save file locally for ingestion
    upload_dir = "datas"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    state = init_state()
    state["resume_text"] = file.filename # Simple track
    
    # Initialize MCP
    client = get_mcp_client()
    await client.connect()
    
    try:
        # 1. Analyze Resume
        state = await resume_analyzer_node(state)
        
        # 2. Get First Question
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
        await client.close()
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
