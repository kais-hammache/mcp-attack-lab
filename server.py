from mcp.server.mcpserver import MCPServer
import os
from pathlib import Path
from mcp.server.mcpserver.tools import base


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


@mcp.tool()
def read_path_safe(path: str) -> str:
    """Read a file from the sandbox directory and return its content.
    Paths outside the sandbox are rejected."""
    base = Path("sandbox").resolve()
    cible = (base / path).resolve()
    if not cible.is_relative_to(base):
        return "Error: access denied"
    try:
        with open(cible) as f:
            return f.read()
    except FileNotFoundError:
        return "Error: file not found."


mcp.run()
