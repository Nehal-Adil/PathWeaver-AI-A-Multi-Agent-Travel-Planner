import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key= GROQ_API_KEY
)

client = MultiServerMCPClient(
    {
        # Remote MCP server for Tavily API
        "tavily": {
            "transport": "streamable_http",
            "url": f"https://mcp.tavily.com/mcp/",
            "headers": {
                "Authorization": f"Bearer {TAVILY_API_KEY}"
            }
        },
        # Local MCP server for Aviationstack API
        "Aviationstack MCP": {
            "transport": "stdio",
            "command": "uvx",
            "args": [
                "aviationstack-mcp"
            ],
            "env": {
                "AVIATION_STACK_API_KEY": AVIATIONSTACK_API_KEY
            }
        },
        # Custom MCP server for OpenWeather API
        "Weather MCP": {
            "transport": "stdio",
            "command": "D:\\Work\\AI\\Agentic AI\\Projects\\PathWeaver AI - A Multi-Agent Travel Planner\\.venv\\Scripts\\python.exe",
            "args": [
                "-u",
                "D:\Work\AI\Agentic AI\Projects\PathWeaver AI - A Multi-Agent Travel Planner\src\custom_weather_mcp_server.py"
            ],
            "env": {
                "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY,
                "PYTHONBUFFERED": "1"
            },
        }
    }
)

async def get_all_tools():
    tools = await client.get_tools()
    print("\nAvailable MCP tools:")
    
    for tool in tools:
        print(tool.name)

# ######################################
# Tavily and Aviation Tool
# ######################################

search_tool = None
aviation_tools = {}

async def initialize_mcp():

    global search_tool
    global aviation_tools

    if search_tool is not None:
        return

    tools = await client.get_tools()

    print("\nAvailable MCP tools:")

    for tool in tools:
        print(tool.name)

    search_tool = next(
        tool
        for tool in tools
        if tool.name == "tavily_search"
    )

    aviation_tools = {
        tool.name: tool
        for tool in tools
        if tool.name != "tavily_search"
    }

async def tavily_mcp_search(query: str):
    await initialize_mcp()

    result = await search_tool.ainvoke(
        {
            "query": query
        }
    )
    return result

async def aviation_mcp_search(tool_name: str, tool_args: dict = None):
    tools = await client.get_tools()

    tool = next(
        t for t in tools
        if t.name == tool_name
    )

    result = await tool.ainvoke(tool_args or {})

    return result

# ######################################
# Weather Tool
# ######################################

weather_tool = None
forecast_tool = None

async def initialize_weather_tools():
    global weather_tool
    global forecast_tool

    if weather_tool is not None and forecast_tool is not None:
        return  

    tools = await client.get_tools()

    print("\nAvailable Weather MCP tools:")

    for tool in tools:
        print(tool.name)

    weather_tool = next(
        tool
        for tool in tools
        if tool.name == "get_current_weather"
    )

    forecast_tool = next(
        tool
        for tool in tools
        if tool.name == "get_forecast"
    )

async def weather_mcp_search(city: str):
    await initialize_weather_tools()

    result = await weather_tool.ainvoke(
        {
            "city": city
        }
    )
    return result

async def forecast_mcp_search(city: str):
    await initialize_weather_tools()

    result = await forecast_tool.ainvoke(
        {
            "city": city
        }
    )
    return result


####################################
# Destination Extractor
####################################

def extract_destination(query: str):
    prompt = """
    Extract only the destination city or country.

    Query: {query}

    Return only destination name.

    """

    response = llm.invoke(prompt)

    return response.content.strip()

