from utils.llm import get_llm


def evaluator_agent(state):

    llm = get_llm()

    question = state["current_question"]
    answer = state["candidate_answer"]

    prompt = f"""
You are an HR Manager evaluating a candidate's performance in an initial screening call.

Evaluate the candidate based on:
1. Communication Skills: Clarity, tone, and professionalism.
2. Interest Level: Enthusiasm for the role and company.
3. Cultural Fit: How well they align with a professional work environment.

Question:
{question}

Answer:
{answer}

Return:
score (0-10)
feedback (Focus on communication and fit, not technical depth)
"""

    response = llm.invoke(prompt)

    print("\nEvaluation:")
    print(response.content)

    state["evaluation"] = response.content

    return state