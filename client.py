import asyncio
from mcp import ClientSession, StdioServerParameters, server
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
import anthropic


load_dotenv()
llm = anthropic.Anthropic()
user_message = "What does the file notes.txt contain?"


async def main():
    params = StdioServerParameters(command="python", args=["server.py"])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            anthropic_tools = []
            for tool in tools.tools:
                mcp_tool = {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.input_schema,
                }
                anthropic_tools.append(mcp_tool)

            response = llm.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=200,
                tools=anthropic_tools,
                messages=[{"role": "user", "content": user_message}],
            )

            for block in response.content:
                if block.type == "tool_use":
                    tool_id = block.id
                    mcp_result = await session.call_tool(block.name, block.input)
                    result = mcp_result.content

            final = llm.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=200,
                tools=anthropic_tools,
                messages=[
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": response.content},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_id,
                                "content": result,
                            }
                        ],
                    },
                ],
            )
            print(final)


asyncio.run(main())
