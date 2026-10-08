import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio


CANARY = "CANARY-7f3a9"
PATH_CHARGES = ["../secret.txt", os.path.abspath("secret.txt"), "notes.txt"]
PATH_TOOLS = ["read_path", "read_path_safe"]


CMD_CHARGES = ["localhost", "; cat secret.txt"]
CMD_TOOLS = ["ping_host", "ping_host_safe"]


async def main():

    params = StdioServerParameters(command="python3", args=["server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            for tool_name in PATH_TOOLS:
                print("TEST: ", tool_name)
                for charge in PATH_CHARGES:
                    result = await session.call_tool(tool_name, {"path": charge})
                    if CANARY in result.content[0].text:
                        print("VULNERABLE: ", charge)
                    else:
                        print("OK: ", charge)
                print()

            for tool_name in CMD_TOOLS:
                print("TEST: ", tool_name)
                for charge in CMD_CHARGES:
                    result = await session.call_tool(tool_name, {"host": charge})
                    if CANARY in result.content[0].text:
                        print("VULNERABLE: ", charge)
                    else:
                        print("OK: ", charge)
                print()


asyncio.run(main())
