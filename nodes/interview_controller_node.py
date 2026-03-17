def interview_controller_node(state):

    # Use question_index to track total questions asked (Interviewer + Followups)
    count = state["question_index"]

    max_questions = 2

    if count >= max_questions:
        state["interview_complete"] = True
    else:
        state["interview_complete"] = False

    return state