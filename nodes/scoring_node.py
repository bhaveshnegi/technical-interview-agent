def scoring_node(state):

    answer = state["candidate_answer"]

    score = len(answer.split()) // 5

    if score > 10:
        score = 10

    feedback = "Good explanation" if score > 5 else "Answer needs more depth"

    state["score"] = score
    state["feedback"] = feedback

    print(f"\nScore: {score}/10")
    print(f"Feedback: {feedback}")

    return state