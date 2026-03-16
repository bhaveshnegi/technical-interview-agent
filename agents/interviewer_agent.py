from utils.llm import get_llm
from tools.resume_retriever_tool import resume_retriever_tool


def interviewer_agent(state):

    llm = get_llm()

    index = state["resume_index"]

    context = resume_retriever_tool(
        index,
        "candidate projects and skills"
    )

    history = state["conversation_history"]

    prompt = f"""
You are a senior technical interviewer.

Candidate resume context:
{context}

Previous conversation:
{history}

Ask ONE technical interview question based on the resume.
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