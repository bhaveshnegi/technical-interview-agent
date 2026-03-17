import sys
import os
from mcp.server.fastmcp import FastMCP
import json

# Ensure the project root is in sys.path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

try:
    from mcp_server.tools_registry import get_tools
except (ImportError, ModuleNotFoundError):
    from tools_registry import get_tools

# Create a FastMCP server instance
mcp = FastMCP("Technical Interview Agent")

# Register tools from the registry
tools = get_tools()
# for tool_info in tools:
#     @mcp.tool(name=tool_info["name"], description=tool_info["description"])
#     def registered_tool(*args, **kwargs):
#         # This is a wrapper to register tools dynamically
#         # Since FastMCP uses decorators, we need to be careful with how we register
#         # In a real scenario, we might want to use mcp.add_tool if available
#         # or define them explicitly for better type hint support.
#         pass

# Explicitly register tools for better clarity and type handling in FastMCP
@mcp.tool()
def analyze_resume() -> str:
    """Analyzes the stored resume to extract technical skills and projects.
    Loads the vector store from disk so no non-serialisable objects need to
    be passed over the MCP stdio transport.
    """
    from services.resume_ingestion import get_chroma_vector_store, get_index
    from tools.resume_analyzer_tool import analyze_resume as analyze_func

    vector_store = get_chroma_vector_store("vector_store")
    index = get_index(vector_store)
    return json.dumps(analyze_func(index))

@mcp.tool()
def hr_scoring_tool(interview_data: dict) -> dict:
    """Computes a structured HR screening scorecard based on provided interview data."""
    from tools.scoring_tool import hr_scoring_tool as score_func
    return json.dumps(score_func(interview_data))

@mcp.tool()
def vector_search(query: str, vector_store_path: str = "vector_store") -> str:
    """Performs a semantic search on the candidate's resume to find relevant context."""
    from tools.vector_search_tool import vector_search as search_func
    return search_func(query, vector_store_path)

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()
