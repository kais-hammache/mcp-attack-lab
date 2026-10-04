from mcp.server.mcpserver import MCPServer


mcp = MCPServer("files")


FAKE_FILES = {"notes.txt": "Buy milk. Call Alice."}


@mcp.tool()
def read_path(path: str) -> str:
    """Read a file from the fake file system and return its content."""
    if path not in FAKE_FILES:
        return "Error: file not found"
    return FAKE_FILES[path]


mcp.run()
