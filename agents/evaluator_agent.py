from utils.llm import get_llm


def evaluator_agent(state):

    llm = get_llm()

    question = state["current_question"]
    answer = state["candidate_answer"]

    prompt = f"""
You are a technical hr interviewer. Ask questions about the candidate's projects or skills. This is for Associate level (fresher)role.

Evaluate the candidate answer.

Question:
{question}

Answer:
{answer}

Return:
score (0-10)
feedback
"""

    response = llm.invoke(prompt)

    print("\nEvaluation:")
    print(response.content)

    state["evaluation"] = response.content

    return state