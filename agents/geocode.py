from graph.state import RouteState
from tools.geocode_tool import geocode


def geocode_node(state: RouteState):

    source = geocode.invoke(state["source"])
    destination = geocode.invoke(state["destination"])

    return {
        "source_coords": source,
        "destination_coords": destination
    }