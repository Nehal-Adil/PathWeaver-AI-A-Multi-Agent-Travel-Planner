import asyncio
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools.mcp_search_client import tavily_mcp_search, get_tavily_search_tool

load_dotenv()  # reads GROQ_API_KEY from your .env file

async def main():
    tools = await get_tavily_search_tool()
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

    agent = create_agent(
        llm,
        tools,
        system_prompt="You are a hotel research assistant. Use search to find real, current hotels.",
    )

    result = await agent.ainvoke(
        {"messages": [("user", "Find 3 good hotels in Goa under ₹5000 per night")]}
    )
    print(result["messages"][-1].content)

asyncio.run(main())