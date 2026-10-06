from mcp.server.mcpserver import MCPServer
import os


mcp = MCPServer("files")


@mcp.tool()
def read_path(path: str) -> str:
    """Read a file from the sandbox directory and return its content."""
    full_path = os.path.join("sandbox", path)
    try:
        with open(full_path) as f:
            return f.read()
    except FileNotFoundError:
        return "Error: file not found"


mcp.run()
