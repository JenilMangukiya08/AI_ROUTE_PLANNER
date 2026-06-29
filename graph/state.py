from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class RouteState(TypedDict):

    messages: Annotated[list, add_messages]

    source: str
    source_coords: dict
    destination: str
    destination_coords: dict
    weather: dict
    route: dict
    traffic: dict
    report: str
    decision: dict