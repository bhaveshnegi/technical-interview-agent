import json
import re
from utils.llm import get_llm

async def resume_analyzer_agent(resume_text: str):
    """
    Uses an LLM to extract structured data (skills and projects) from raw resume text.
    """
    llm = get_llm()

    prompt = f"""
You are an expert HR Data Analyst. Your task is to extract technical skills and projects from the provided resume text.

Resume Text:
{resume_text}

Instructions:
1. Extract a simple list of technical skills (languages, frameworks, tools, etc.).
2. Extract a list of significant projects (title and a brief one-sentence description if possible).
3. If no skills or projects are found, return empty lists.

Return the result in the following JSON format ONLY:
{{
  "skills": ["skill1", "skill2"],
  "projects": ["Project Title: Description", "Another Project: Description"]
}}
"""

    response = llm.invoke(prompt)
    content = response.content

    # Extract JSON from response
    try:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {"skills": [], "projects": []}
    except Exception:
        result = {"skills": [], "projects": []}

    return result
