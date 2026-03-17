from mcp_client import get_mcp_client
import json

async def resume_analyzer_node(state):

    print("\nAnalyzing resume...")

    client = get_mcp_client()

    # Call analyze_resume via MCP.
    # The server-side tool loads the vector store itself so no non-serialisable
    # index object needs to be passed over the stdio transport.
    mcp_response = await client.call_tool("analyze_resume", {})

    result = {"skills": [], "projects": []}
    if mcp_response.content:
        raw = mcp_response.content[0].text
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            print(f"[resume_analyzer_node] WARNING: could not parse MCP response as JSON. Raw: {repr(raw)}")

    state["skills"] = result.get("skills", [])
    state["projects"] = result.get("projects", [])

    print("\nExtracted Skills:")
    for skill in state["skills"]:
        print("-", skill)

    print("\nExtracted Projects:")
    for project in state["projects"]:
        print("-", project)

    return state