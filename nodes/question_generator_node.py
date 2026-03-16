def question_generator_node(state):

    skills = state["skills"]

    questions = []

    for skill in skills:
        questions.append(f"Explain your experience with {skill}")

    if not questions:
        questions.append("Tell me about yourself")

    state["question_list"] = questions
    state["question_index"] = 0

    return state