from utils.llm import get_llm


def interviewer_agent(state):

    llm = get_llm()

    skills = state["skills"]
    projects = state["projects"]
    history = state["conversation_history"]

    prompt = f"""
You are an expert technical recruiter. Ask questions about the candidate's projects or skills. This is for Associate level (fresher)role.

Candidate Skills:
{skills}

Candidate Projects:
{projects}

Previous conversation:
{history}

Ask exactly ONE technical interview question based on the resume.Very simple questions.Like what, how, why, etc. and your experience with it.

For example:
If candidate has mentioned "Machine Learning" in skills, ask "what is Machine Learning?"
If candidate has mentioned "RAG" in skills, ask "what is RAG?"



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

    # Track every question asked
    state["question_index"] += 1

    return state