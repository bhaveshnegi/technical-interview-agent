from utils.llm import get_llm


def followup_agent(state):

    llm = get_llm()

    question = state["current_question"]
    answer = state["candidate_answer"]

    prompt = f"""
Based on the answer below, ask a deeper follow-up question.

Question:
{question}

Answer:
{answer}
"""

    response = llm.invoke(prompt)

    followup = response.content

    print("\nFollow-up Question:", followup)

    answer = input("\nCandidate: ")

    state["candidate_answer"] = answer

    return state