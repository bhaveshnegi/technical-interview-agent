def ask_question_node(state):

    index = state["question_index"]
    questions = state["question_list"]

    if index >= len(questions):
        state["interview_complete"] = True
        return state

    question = questions[index]

    print("\nAgent:", question)

    answer = input("\nCandidate: ")

    state["current_question"] = question
    state["candidate_answer"] = answer

    return state