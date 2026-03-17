import unittest
from mcp_server.mcp_server import mcp

class TestMCPServer(unittest.TestCase):
    def test_tools_registration(self):
        """Verify that the expected tools are registered with the MCP server."""
        # Get the list of registered tools from the FastMCP instance
        # FastMCP stores tools in its internal registry
        registered_tools = mcp._tool_manager.list_tools()
        tool_names = [tool.name for tool in registered_tools]
        
        expected_tools = ["analyze_resume", "hr_scoring_tool", "vector_search"]
        
        for tool in expected_tools:
            self.assertIn(tool, tool_names, f"Tool {tool} should be registered")
            print(f"Verified tool: {tool}")

if __name__ == "__main__":
    unittest.main()
