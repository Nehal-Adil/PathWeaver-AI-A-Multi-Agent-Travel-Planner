from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tavily", port=8001)

async def web_search(query: str) -> str:
    result = await mcp.call("search", query)
    return result

if __name__ == "__main__":
    mcp.run(transport="streamable-http")