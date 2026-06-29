from graph.state import RouteState
from tools.weather_tool import get_weather


def weather_node(state: RouteState):

    dest = state["destination_coords"]

    weather = get_weather.invoke({
        "lat": dest["latitude"],
        "lon": dest["longitude"]
    })

    return {
        "weather": weather
    }