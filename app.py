import asyncio
from graphs.interview_graph import build_graph
from services.resume_ingestion import get_chroma_vector_store, get_index
from mcp_client import get_mcp_client

async def main():

    print("Loading existing resume index...")

    vector_store = get_chroma_vector_store("vector_store")

    index = get_index(vector_store)

    graph = build_graph()

    state = {
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
        "resume_index": index
    }

    # Eagerly connect to MCP server BEFORE graph starts.
    # This avoids anyio cancel-scope violations that occur when the client
    # lazy-connects from inside a LangGraph sub-task (asyncio.create_task).
    client = get_mcp_client()
    await client.connect()

    try:
        await graph.ainvoke(state)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())