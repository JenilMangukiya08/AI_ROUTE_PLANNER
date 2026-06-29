import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")


def reverse_geocode(lat: float, lon: float):
    """
    Reverse geocode GPS coordinates into a readable address.
    """

    url = f"https://api.tomtom.com/search/2/reverseGeocode/{lat},{lon}.json"

    params = {
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    return data["addresses"][0]["address"]["freeformAddress"]

