import re
from tools.resume_retriever_tool import resume_retriever_tool


def extract_section(text, section_keywords):

    lines = text.split("\n")

    results = []
    capture = False

    stop_keywords = [
        "project",
        "experience",
        "education",
        "academic",
        "certificate"
    ]

    for line in lines:

        l = line.lower().strip()

        # start capturing
        if any(k in l for k in section_keywords):
            capture = True
            continue

        # stop if new section appears
        if capture and any(k in l for k in stop_keywords):
            break

        if capture:
            line = line.strip()

            if not line:
                continue

            # remove bullets
            line = re.sub(r"^[•\-o]\s*", "", line)

            results.append(line)

    return results


def analyze_resume(index):

    context_skills = resume_retriever_tool(index, "technical skills only")
    context_projects = resume_retriever_tool(index, "projects only")

    skills = extract_section(
        context_skills,
        ["technical skills", "skills"]
    )

    projects = extract_section(
        context_projects,
        ["projects", "project"]
    )

    return {
        "skills": skills,
        "projects": projects
    }