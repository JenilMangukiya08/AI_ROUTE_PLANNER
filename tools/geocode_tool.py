import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from langchain_core.tools import tool
from langsmith import traceable
load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")


@tool
@traceable(name="Geocode Tool")
def geocode(location: str) -> dict:
    """
    Convert a place name into latitude and longitude using TomTom.
    """

    location = quote(f"{location}, India")

    url = f"https://api.tomtom.com/search/2/geocode/{location}.json"

    params = {
        "key": API_KEY,
        "limit": 1,
        "countrySet": "IN"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if not data["results"]:
            return {
                "error": "Location not found."
            }

        result = data["results"][0]

        return {
            "address": result["address"]["freeformAddress"],
            "latitude": result["position"]["lat"],
            "longitude": result["position"]["lon"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }