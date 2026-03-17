from utils.llm import get_llm
import json
import re
from tools.scoring_tool import hr_scoring_tool

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

Return the evaluation in the following JSON format ONLY:
{{
  "communication_score": (int 0-10),
  "communication_feedback": "string",
  "interest_score": (int 0-10),
  "interest_feedback": "string",
  "cultural_fit_score": (int 0-10),
  "cultural_fit_feedback": "string"
}}
"""

    response = llm.invoke(prompt)
    content = response.content

    # Extract JSON from response
    try:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            eval_data = json.loads(json_match.group())
        else:
            # Fallback if no JSON found
            eval_data = {
                "communication_score": 5,
                "communication_feedback": "Likely conversational, but system failed to parse structured feedback.",
                "interest_score": 5,
                "interest_feedback": "N/A",
                "cultural_fit_score": 5,
                "cultural_fit_feedback": "N/A"
            }
    except Exception:
        eval_data = {
            "communication_score": 0,
            "communication_feedback": "Error parsing evaluation result.",
            "interest_score": 0,
            "interest_feedback": "Error",
            "cultural_fit_score": 0,
            "cultural_fit_feedback": "Error"
        }

    # Use the scoring tool
    scorecard = hr_scoring_tool(eval_data)

    print("\n--- HR Screening Scorecard ---")
    for category, result in scorecard.items():
        if isinstance(result, dict):
            print(f"{category}: Score {result['score']}/10 - {result['feedback']}")
        else:
            print(f"{category}: {result}")

    state["evaluation"] = scorecard

    return state