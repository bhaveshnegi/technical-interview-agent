from utils.llm import get_llm
from mcp_client import get_mcp_client

async def interviewer_agent(state):

    llm = get_llm()
    client = get_mcp_client()

    skills = state["skills"]
    projects = state["projects"]
    history = state["conversation_history"]
    
    # Proactively search for more context if history is not empty
    resume_context = ""
    if len(history) > 0:
        # Search for something relevant to the current conversation or general resume facts
        # Use MCP tool instead of direct import
        mcp_response = await client.call_tool("vector_search", {"query": "What are the candidate's achievements and work experience details?"})
        resume_context = mcp_response.content[0].text if mcp_response.content else ""

    prompt = f"""
You are an HR Recruiter conducting an initial screening call (HR Screening Round). 
Your goal is to be friendly, conversational, and filter the candidate for a fresher (Associate level) role.

IMPORTANT:
You are talking to a candidate in REAL-TIME.
You must behave like a human interviewer, not like an AI generating lists.

Candidate Skills:
{skills}

Candidate Projects:
{projects}

Additional Resume Context:
{resume_context}

Previous conversation:
{history}

STRICT RULES:
- Ask ONLY ONE question.
- Do NOT generate multiple questions.
- Do NOT give options or suggestions.
- Do NOT explain anything.
- Do NOT say "here are some questions".
- Output must be exactly ONE sentence question.

Rules:
1. Ask exactly ONE light, conversational screening question.
2. If this is the start of the conversation (history is empty), start with a warm welcome and ask "Tell me a bit about yourself and why you're interested in this role?"
3. If history is not empty, ask about their experience with a specific project, their availability, location preference, or what they are looking for in their first job.
4. Avoid deep technical questions (RAG, Machine Learning, etc.). Keep it high-level.
5. Do NOT ask for code or deep technical explanations.
6. Return only the question text.

FLOW:
- If conversation is empty → greet and ask for introduction.
- Otherwise → ask next logical HR question (experience, motivation, availability, etc.)

GOOD EXAMPLE:
"Hi Bhavesh, thanks for joining. Can you briefly introduce yourself?"

BAD EXAMPLE (NEVER DO THIS):
"Here are some questions you can ask..."

Now ask the next question.
"""

    response = llm.invoke(prompt)

    question = response.content

    print("\nInterviewer:", question)

    # Use await for input in a real async environment if needed, 
    # but for study/CLI tool input() is fine although it blocks.
    # In a full async app, we'd use an async input handler.
    answer = input("\nCandidate: ")

    state["current_question"] = question
    state["candidate_answer"] = answer

    state["conversation_history"].append(
        f"Q: {question}\nA: {answer}"
    )

    # Track every question asked
    state["question_index"] += 1

    return state