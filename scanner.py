import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio


CANARY = "CANARY-7f3a9"
CHARGES = ["../secret.txt", os.path.abspath("secret.txt"), "notes.txt"]
TOOLS = ["read_path", "read_path_safe"]


async def main():

    params = StdioServerParameters(command="python3", args=["server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            for tool_name in TOOLS:
                print("TEST: ", tool_name)
                for charge in CHARGES:
                    result = await session.call_tool(tool_name, {"path": charge})
                    if CANARY in result.content[0].text:
                        print("VULNERABLE: ", charge)
                    else:
                        print("OK: ", charge)
                print()


asyncio.run(main())
