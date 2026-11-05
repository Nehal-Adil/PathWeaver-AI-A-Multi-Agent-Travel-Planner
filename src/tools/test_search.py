import asyncio
from tools.mcp_search_client import get_all_tools

async def main():
    tools = await get_all_tools()
    for tool in tools:
        print(f"Tool name: {tool.name}, Tool description: {tool.description}")

    search = next(tool for tool in tools if tool.name == "tavily_search")
    result = await search.ainvoke({"query": "What is the result of midterm elections in the US?"})
    print(f"Search result: {result}")

asyncio.run(main())