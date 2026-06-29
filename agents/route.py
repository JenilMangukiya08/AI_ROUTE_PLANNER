from graph.state import RouteState
from tools.route_tool import get_route


def route_node(state: RouteState):

    src = state["source_coords"]
    dst = state["destination_coords"]

    route = get_route.invoke({
        "start_lat": src["latitude"],
        "start_lon": src["longitude"],
        "end_lat": dst["latitude"],
        "end_lon": dst["longitude"]
    })

    return {
        "route": route
    }
