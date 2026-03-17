from tools.resume_analyzer_tool import analyze_resume
from tools.scoring_tool import hr_scoring_tool
from tools.vector_search_tool import vector_search

def get_tools():
    """Returns a list of tools to be registered with the MCP server."""
    return [
        {
            "name": "analyze_resume",
            "description": "Analyzes a resume to extract technical skills and projects.",
            "func": analyze_resume,
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {
                        "type": "string",
                        "description": "The search index or context for the resume retriever."
                    }
                },
                "required": ["index"]
            }
        },
        {
            "name": "hr_scoring_tool",
            "description": "Computes a structured HR screening scorecard based on provided interview data.",
            "func": hr_scoring_tool,
            "parameters": {
                "type": "object",
                "properties": {
                    "interview_data": {
                        "type": "object",
                        "properties": {
                            "communication_score": {"type": "integer"},
                            "communication_feedback": {"type": "string"},
                            "interest_score": {"type": "integer"},
                            "interest_feedback": {"type": "string"},
                            "cultural_fit_score": {"type": "integer"},
                            "cultural_fit_feedback": {"type": "string"}
                        },
                        "required": ["communication_score", "interest_score", "cultural_fit_score"]
                    }
                },
                "required": ["interview_data"]
            }
        },
        {
            "name": "vector_search",
            "description": "Performs a semantic search on the candidate's resume to find relevant context.",
            "func": vector_search,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query (e.g., 'Tell me about the candidate's internship')."
                    },
                    "vector_store_path": {
                        "type": "string",
                        "description": "Path to the persistent chroma vector store.",
                        "default": "vector_store"
                    }
                },
                "required": ["query"]
            }
        }
    ]
