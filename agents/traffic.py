from graph.state import RouteState
from tools.traffic_tool import get_traffic


def traffic_node(state: RouteState):

    src = state["source_coords"]
    dst = state["destination_coords"]

    traffic = get_traffic.invoke({

        "min_lat": min(src["latitude"], dst["latitude"]),
        "min_lon": min(src["longitude"], dst["longitude"]),

        "max_lat": max(src["latitude"], dst["latitude"]),
        "max_lon": max(src["longitude"], dst["longitude"])

    })

    return {
        "traffic": traffic
    }