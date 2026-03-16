from utils.llm import get_llm


def followup_agent(state):

    llm = get_llm()

    question = state["current_question"]
    answer = state["candidate_answer"]

    prompt = f"""
Based on the answer below, ask a follow-up question. Very simple questions.Like what, how, why, etc. and your experience with it.

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
    
    # Record follow-up interaction in history
    state["conversation_history"].append(
        f"Follow-up Q: {followup}\nA: {answer}"
    )
    
    # Track every question asked
    state["question_index"] += 1

    return state