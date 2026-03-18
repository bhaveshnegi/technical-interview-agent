import asyncio
from agents.interviewer_agent import interviewer_agent
from agents.evaluator_agent import evaluator_agent
from agents.followup_agent import followup_agent
from agents.report_agent import report_agent

def calculate_score(evaluation):
    if not evaluation:
        return 0
    
    scores = []
    # In evaluator_agent, the scorecard keys depend on the hr_scoring_tool output.
    # Typically it has categories with 'score'.
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

        # If we reached the target number of questions, end
        if state["question_index"] >= 2:
            return "end"

        return "ask"

    if last_action == "followup":
        # After follow-up, evaluate the answer to the follow-up
        return "evaluate"

    return "end"

async def orchestrator(state):
    max_steps = 20
    steps = 0

    print("\n--- Interview Started ---")

    while steps < max_steps:
        steps += 1
        step = decide_next_step(state)

        if step == "ask":
            question = await interviewer_agent(state)
            print(f"\nInterviewer: {question}")
            
            answer = input("\nCandidate: ")
            
            state["current_question"] = question
            state["candidate_answer"] = answer
            state["conversation_history"].append(f"Q: {question}\nA: {answer}")
            state["question_index"] += 1
            state["last_action"] = "ask"

        elif step == "evaluate":
            print("\nEvaluating answer...")
            state = await evaluator_agent(state)
            
            evaluation = state.get("evaluation", {})
            print("--- HR Screening Scorecard ---")
            for category, result in evaluation.items():
                if isinstance(result, dict):
                    print(f"{category}: Score {result.get('score', 0)}/10 - {result.get('feedback', 'N/A')}")
                else:
                    print(f"{category}: {result}")
            
            state["last_action"] = "evaluate"

        elif step == "followup":
            question = await followup_agent(state)
            print(f"\nFollow-up: {question}")
            
            answer = input("\nCandidate: ")
            
            state["candidate_answer"] = answer
            state["conversation_history"].append(f"Follow-up Q: {question}\nA: {answer}")
            # Note: We don't increment question_index for follow-up in the user's pseudo-code logic,
            # or maybe we should? The pseudo-code had `state["question_index"] += 1` in followup too.
            # I will follow the pseudo-code.
            state["question_index"] += 1
            state["last_action"] = "followup"

        elif step == "end":
            print("\nGenerating final report...")
            state = await report_agent(state)
            
            report = state.get("final_report")
            print("\n--- FINAL CANDIDATE EVALUATION REPORT ---")
            print(report)
            print("------------------------------------------")
            break

    if steps >= max_steps:
        print("\nReached max steps guard. Ending interview.")

    return state
