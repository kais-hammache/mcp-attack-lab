from mcp.server.mcpserver import MCPServer
import os
from pathlib import Path
import subprocess

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


@mcp.tool()
def ping_host(host: str) -> str:
    """Ping a host and return the result."""
    output = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True,
    )
    return output.stdout + output.stderr


@mcp.tool()
def ping_host_safe(host: str) -> str:
    """Ping a host and return the result. Uses an argument list, not a shell."""
    output = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
    return output.stdout + output.stderr


mcp.run()
