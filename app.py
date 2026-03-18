import asyncio
from orchestrator import orchestrator
from nodes.resume_analyzer_node import resume_analyzer_node
from mcp_client import get_mcp_client

def init_state():
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

async def main():
    print("Initializing Interview System...")

    state = init_state()

    client = get_mcp_client()
    await client.connect()

    try:
        # Step 1: Analyze Resume
        state = await resume_analyzer_node(state)

        # Step 2: Start Orchestrator
        final_state = await orchestrator(state)
        
        print("\nInterview completed successfully.")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())