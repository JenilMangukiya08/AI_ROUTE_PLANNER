import os
import requests
from langsmith import traceable
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@tool
@traceable(name="Weather Tool")
def get_weather(lat: float, lon: float):
    """
    Get current weather and rain forecast using OpenWeather.
    """

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        forecasts = []

        for item in data["list"][:8]:
            forecasts.append({
                "time": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "weather": item["weather"][0]["description"],
                "rain": item.get("rain", {}).get("3h", 0)
            })

        return forecasts

    except Exception as e:
        return {"error": str(e)}