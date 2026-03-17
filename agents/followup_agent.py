from utils.llm import get_llm


def followup_agent(state):

    llm = get_llm()

    question = state["current_question"]
    answer = state["candidate_answer"]

    prompt = f"""
You are an HR Recruiter conducting an initial screening call. 
Based on the candidate's previous answer, ask a light and professional follow-up question.

The goal is to understand their background, interest, or cultural fit better without digging into deep technical details.

Question:
{question}

Answer:
{answer}

STRICT RULES:
- Ask ONLY ONE question.
- Do NOT generate multiple questions.
- Do NOT give options or suggestions.
- Do NOT explain anything.
- Do NOT say "here are some questions".
- Output must be exactly ONE sentence question.

Rules:
1. Ask exactly ONE conversational follow-up question.
2. Keep the tone friendly and professional.
3. Do NOT ask for technical implementations or deep dives.
4. Return only the question text.
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