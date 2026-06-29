import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from langsmith import traceable
load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")


@tool
@traceable(name="Traffic Tool")
def get_traffic(
    min_lat: float,
    min_lon: float,
    max_lat: float,
    max_lon: float
) -> dict:
    """
    Get live traffic incidents in a bounding box.
    """

    url = "https://api.tomtom.com/traffic/services/5/incidentDetails"

    params = {
        "key": API_KEY,
        "bbox": f"{min_lon},{min_lat},{max_lon},{max_lat}",
        "fields": "{incidents{type,geometry{type,coordinates},properties{iconCategory,delay,events{description}}}}",
        "language": "en-GB",
        "timeValidityFilter": "present"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        incidents = data.get("incidents", [])

        result = []

        for incident in incidents:
            result.append(
                {
                    "type": incident["properties"]["iconCategory"],
                    "delay": incident["properties"].get("delay", 0),
                    "description": incident["properties"]["events"][0]["description"]
                    if incident["properties"].get("events")
                    else "Unknown"
                }
            )

        return {
            "count": len(result),
            "incidents": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }