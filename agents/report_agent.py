from utils.llm import get_llm


async def report_agent(state):

    llm = get_llm()

    history = state["conversation_history"]
    evaluation = state.get("evaluation") or {}

    prompt = f"""
You are an HR Manager writing a final summary report for a candidate's initial screening call.

Review the conversation and the HR scorecard:

Conversation:
{history}

HR Scorecard:
{evaluation}

3. Strengths (bullet points)
4. Weaknesses (bullet points)
5. Final Score (on a scale of 0-10)
6. Recommendation (Hire / Consider / Reject)

Be professional and objective.
"""

    response = llm.invoke(prompt)
    report = response.content

    state["final_report"] = report
    return state
