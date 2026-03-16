from utils.llm import get_llm


def interviewer_agent(state):

    llm = get_llm()

    skills = state["skills"]
    projects = state["projects"]
    history = state["conversation_history"]

    prompt = f"""
You are a technical hr interviewer. Ask questions about the candidate's projects or skills. This is for Associate level (fresher)role.

Candidate Skills:
{skills}

Candidate Projects:
{projects}

Previous conversation:
{history}

Ask exactly ONE technical interview question based on the resume.

For example:
If candidate has mentioned "Python" in skills, ask "Tell me about your experience with Python."

Rules:
- Ask only ONE question.
- Do NOT add follow-up questions.
- Do NOT add explanations.
- Return only the question text.
"""

    response = llm.invoke(prompt)

    question = response.content

    print("\nInterviewer:", question)

    answer = input("\nCandidate: ")

    state["current_question"] = question
    state["candidate_answer"] = answer

    state["conversation_history"].append(
        f"Q: {question}\nA: {answer}"
    )

    return state