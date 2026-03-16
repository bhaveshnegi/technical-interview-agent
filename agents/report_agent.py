from utils.llm import get_llm

def report_agent(state):
    llm = get_llm()

    history = state.get("conversation_history", [])
    # In some nodes it might be stored as 'evaluation' or used from 'score'/'feedback'
    # Based on evaluator_agent.py, it's state["evaluation"]
    evaluation = state.get("evaluation", "No evaluation available.")

    prompt = f"""
You are an expert technical recruiter. Based on the interview conversation and evaluation scores, 
generate a final candidate assessment report.

### Interview History:
{history}

### Detailed Evaluation:
{evaluation}

### Report Requirements:
Generate a report with the following sections:
1. Candidate Evaluation Report
2. Candidate Name (from context if available, otherwise use "Candidate")
3. Strengths (bullet points)
4. Weaknesses (bullet points)
5. Final Score (on a scale of 0-10)
6. Recommendation (Hire / Consider / Reject)

Be professional and objective.
"""

    response = llm.invoke(prompt)
    report = response.content

    print("\n--- FINAL CANDIDATE EVALUATION REPORT ---")
    print(report)
    print("------------------------------------------")

    state["final_report"] = report
    return state
