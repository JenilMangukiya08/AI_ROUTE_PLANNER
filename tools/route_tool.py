import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from langsmith import traceable
load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")


@tool
@traceable(name="Route Tool")
def get_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
) -> dict:
    """
    Calculate the best driving route between two coordinates using TomTom.
    """

    url = (
        f"https://api.tomtom.com/routing/1/calculateRoute/"
        f"{start_lat},{start_lon}:{end_lat},{end_lon}/json"
    )

    params = {
        "key": API_KEY,
        "traffic": "true",
        "travelMode": "car",
        "routeType": "fastest",
        "maxAlternatives": 3
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if "routes" not in data:
            return {"error": "No route found"}

        routes = []

        for i, route in enumerate(data["routes"]):

            summary = route["summary"]

            coordinates = []

            for leg in route["legs"]:
                for point in leg["points"]:
                    coordinates.append([
                        point["latitude"],
                        point["longitude"]
                    ])

            routes.append({
                "route_id": i + 1,
                "distance_km": round(summary["lengthInMeters"] / 1000, 2),
                "travel_time_min": round(summary["travelTimeInSeconds"] / 60, 2),
                "traffic_delay_min": round(summary["trafficDelayInSeconds"] / 60, 2),
                "arrival_time": summary["arrivalTime"],
                "departure_time": summary["departureTime"],
                "coordinates": coordinates
            })

        return {
            "routes": routes
        }

    except Exception as e:
        return {"error": str(e)}