import asyncio
from mcp import ClientSession, StdioServerParameters, server
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(command="python", args=["server.py"])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            for tool in tools.tools:
                print(tool.name, "|", tool.description)

            result = await session.call_tool("read_path", {"path": "notes.txt"})
            print(result)


asyncio.run(main())
