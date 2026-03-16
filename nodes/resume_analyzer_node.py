from tools.resume_analyzer_tool import analyze_resume


def resume_analyzer_node(state):

    print("\nAnalyzing resume...")

    index = state["resume_index"]

    result = analyze_resume(index)

    state["skills"] = result["skills"]
    state["projects"] = result["projects"]

    print("\nExtracted Skills:")
    for skill in state["skills"]:
        print("-", skill)

    print("\nExtracted Projects:")
    for project in state["projects"]:
        print("-", project)

    return state