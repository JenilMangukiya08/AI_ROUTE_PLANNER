from agents.decision import decision_node
from agents.report import report_node
from agents.planner import planner_node
from agents.geocode import geocode_node
from agents.route import route_node
from langgraph.graph import StateGraph, START, END
from graph.state import RouteState
from agents.traffic import traffic_node
from agents.weather import weather_node
graph = StateGraph(RouteState)

graph.add_node("planner", planner_node)
graph.add_node("geocode", geocode_node)
graph.add_node("route", route_node)
graph.add_node("traffic", traffic_node)
graph.add_node("weather", weather_node)
graph.add_node("decision", decision_node)
graph.add_node("report", report_node)

graph.add_edge(START, "planner")
graph.add_edge("planner", "geocode")
graph.add_edge("geocode", "route")

graph.add_edge("route", "traffic")
graph.add_edge("route", "weather")

graph.add_edge("traffic", "decision")
graph.add_edge("weather", "decision")

graph.add_edge("decision", "report")
graph.add_edge("report", END)

graph = graph.compile()