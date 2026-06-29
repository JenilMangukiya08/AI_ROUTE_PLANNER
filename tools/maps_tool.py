import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from langsmith import traceable
load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

print(API_KEY)

@tool
@traceable(name="Map Tool")
def get_route(source: str, destination: str) -> dict:
    """
    Get the best driving route between two places.
    """

    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": source,
        "destination": destination,
        "mode": "driving",
        "alternatives": "true",
        "departure_time": "now",
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    if data["status"] != "OK":
        return {
            "error": data["status"]
        }

    route = data["routes"][0]
    leg = route["legs"][0]
   

    return {
        "distance": leg["distance"]["text"],
        "duration": leg["duration"]["text"],
        "start_address": leg["start_address"],
        "end_address": leg["end_address"]
    }
