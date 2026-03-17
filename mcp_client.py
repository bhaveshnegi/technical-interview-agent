import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """A client to interact with the Technical Interview Agent MCP server."""

    def __init__(self):
        self._session = None
        self._stdio_ctx = None
        self._session_ctx = None

    async def connect(self):
        """
        Explicitly connects to the MCP server.
        Must be called from the same asyncio task that will use the client,
        before any LangGraph sub-tasks are spawned (avoids anyio cancel-scope
        task-crossing errors).
        """
        if self._session is not None:
            return  # Already connected

        server_script = os.path.join(os.getcwd(), "mcp_server", "mcp_server.py")
        server_params = StdioServerParameters(
            command="python",
            args=[server_script],
            env=os.environ.copy()
        )

        try:
            self._stdio_ctx = stdio_client(server_params)
            read, write = await self._stdio_ctx.__aenter__()

            self._session_ctx = ClientSession(read, write)
            self._session = await self._session_ctx.__aenter__()

            await self._session.initialize()
        except Exception as e:
            await self.close()
            raise RuntimeError(f"Failed to connect to MCP server: {e}")

    async def get_tools(self):
        """Retrieves the list of available tools from the MCP server."""
        if self._session is None:
            raise RuntimeError("MCPClient is not connected. Call await client.connect() first.")
        result = await self._session.list_tools()
        return result.tools

    async def call_tool(self, tool_name, arguments):
        """Calls a tool on the MCP server."""
        if self._session is None:
            raise RuntimeError("MCPClient is not connected. Call await client.connect() first.")
        return await self._session.call_tool(tool_name, arguments)

    async def close(self):
        """Closes the connection to the MCP server."""
        if self._session_ctx:
            try:
                await self._session_ctx.__aexit__(None, None, None)
            except Exception:
                pass
            self._session_ctx = None
            self._session = None

        if self._stdio_ctx:
            try:
                await self._stdio_ctx.__aexit__(None, None, None)
            except Exception:
                pass
            self._stdio_ctx = None


# Singleton instance
_client = MCPClient()


def get_mcp_client() -> MCPClient:
    """Returns the singleton MCP client instance."""
    return _client
