from tools.tavily_tool import tavily_search
from tools.flight_search_tool import search_flights
from mcp_client import get_all_tools
from backend import run_travel_agent

# res = tavily_search("Best Japanese hotels in Bangalore")
# print(res)

# res = search_flights("Plan a 7 days Japan trip from India.")
# print(res)

# user_input = input("Enter travel request: ")

# response = run_travel_agent(
#     user_input=user_input,
#     thread_id="test_user"
# )
# print("\nFINAL RESPONSE: \n")
# print(response["answer"])


import asyncio
from tools.mcp_search_client import tavily_mcp_search

# if __name__ == "__main__":
#     query = "Summarize the last test match between Australia and Proteas."
#     asyncio.run(tavily_mcp_search(query))

if __name__ == "__main__":
    asyncio.run(get_all_tools())