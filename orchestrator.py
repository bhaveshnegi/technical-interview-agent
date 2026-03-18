import asyncio
from agents.interviewer_agent import interviewer_agent
from agents.evaluator_agent import evaluator_agent
from agents.followup_agent import followup_agent
from agents.report_agent import report_agent

def calculate_score(evaluation):
    if not evaluation:
        return 0
    
    scores = []
    for key, value in evaluation.items():
        if isinstance(value, dict) and 'score' in value:
            scores.append(value['score'])
    
    if not scores:
        return 0
    return sum(scores) / len(scores)

def decide_next_step(state):
    # Initial state
    if state["question_index"] == 0 and state.get("last_action") is None:
        return "ask"

    last_action = state.get("last_action")

    if last_action == "ask":
        return "evaluate"

    if last_action == "evaluate":
        avg_score = calculate_score(state.get("evaluation"))
        
        # If score is low, ask a follow-up
        if avg_score < 5:
            return "followup"

        # If we reached the target number of questions, end (User changed to 2)
        if state["question_index"] >= 2:
            return "end"

        return "ask"

    if last_action == "followup":
        return "evaluate"

    return "end"

async def handle_next_step(state, user_answer=None):
    """
    State machine for the interview. 
    Processes the user's last answer (if provided) and returns the next message for the UI.
    Returns: (updated_state, message_type, message_content)
    message_type: 'question', 'followup', 'report'
    """
    
    # If there's a user answer, we need to update the state before deciding the next step
    if user_answer is not None:
        state["candidate_answer"] = user_answer
        last_action = state.get("last_action")
        
        if last_action == "ask":
            state["conversation_history"].append(f"Q: {state.get('current_question')}\nA: {user_answer}")
        elif last_action == "followup":
            state["conversation_history"].append(f"Follow-up Q: {state.get('current_question')}\nA: {user_answer}")
            
    # Run the loop until we hit a step that requires user input (ask/followup) or end
    while True:
        step = decide_next_step(state)

        if step == "ask":
            question = await interviewer_agent(state)
            state["current_question"] = question
            state["question_index"] += 1
            state["last_action"] = "ask"
            return state, "question", question

        elif step == "evaluate":
            state = await evaluator_agent(state)
            state["last_action"] = "evaluate"
            # Continue loop to next step immediately after evaluation

        elif step == "followup":
            question = await followup_agent(state)
            state["current_question"] = question
            state["question_index"] += 1
            state["last_action"] = "followup"
            return state, "followup", question

        elif step == "end":
            state = await report_agent(state)
            state["last_action"] = "end"
            state["interview_complete"] = True
            return state, "report", state.get("final_report")
