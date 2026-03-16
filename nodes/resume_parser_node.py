def resume_parser_node(state):

    resume_text = state["resume_text"]

    # simple placeholder logic
    skills = []
    projects = []

    if "python" in resume_text.lower():
        skills.append("Python")

    if "machine learning" in resume_text.lower():
        skills.append("Machine Learning")

    if "project" in resume_text.lower():
        projects.append("Detected Project")

    state["skills"] = skills
    state["projects"] = projects

    return state