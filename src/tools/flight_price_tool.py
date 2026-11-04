# tools/flight_search.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def flight_search_tool(departure_iata: str, arrival_iata: str, travel_date: str) -> str:
    """
    Search real-time live flight prices, options, and durations between two airport IATA codes.
    Use this tool whenever a user asks for ticket pricing, flight options, or booking details.
    
    Args:
        departure_iata: The 3-letter IATA code of the starting airport (e.g., "JFK", "CDG", "DAC"). Must be exactly 3 uppercase letters.
        arrival_iata: The 3-letter IATA code of the destination airport (e.g., "AUS", "LHR", "NRT"). Must be exactly 3 uppercase letters.
        travel_date: The date string formatted strictly as YYYY-MM-DD (e.g., "2026-11-20").
    """

    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        return "Error: SERPAPI_API_KEY environment variable is still missing in this context."
    
    # Force uppercase string normalization just in case the LLM sends lowercases
    dep = departure_iata.strip().upper()
    arr = arrival_iata.strip().upper()
    
    print(f"[DEBUG] Executing live flight lookup: {dep} ➔ {arr} on {travel_date}")

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_flights",
        "departure_id": dep,
        "arrival_id": arr,
        "outbound_date": travel_date,
        "currency": "USD",
        "type": "2",  # One-way ticket routing type
        "api_key": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "best_flights" not in data or not data["best_flights"]:
            return f"No direct flights found from {dep} to {arr} on {travel_date}."

        result_string = f"✈️ Live Flight Fares on {travel_date} ({dep} to {arr}):\n"
        
        for i, flight in enumerate(data["best_flights"][:3], 1):
            price = flight.get("price", "N/A")
            airlines = [leg.get("airline", "Unknown") for leg in flight.get("flights", [])]
            airline_name = ", ".join(list(set(airlines)))
            total_duration = flight.get("total_duration", "N/A")
            stops = len(flight.get("flights", [])) - 1
            stops_str = "Non-stop" if stops == 0 else f"{stops} stop(s)"

            result_string += (f"{i}. {airline_name} — ${price} USD\n"
                              f"   Duration: {total_duration} mins | {stops_str}\n")
        
        return result_string

    except Exception as e:
        return f"Error connecting to flight engine: {str(e)}"


if __name__ == "__main__":
    # Simulate exactly how the LLM will invoke your tool!
    # It converts "New York" -> "JFK" and "London" -> "LHR" automatically.
    result = flight_search_tool(
        departure_iata="JFK", 
        arrival_iata="LHR", 
        travel_date="2026-12-15"
    )
    print("\n--- TEST RESULT ---")
    print(result)

