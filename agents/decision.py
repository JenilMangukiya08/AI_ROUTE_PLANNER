import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from graph.state import RouteState
from graph.schema import DecisionSchema
import time
load_dotenv()
from pydantic import BaseModel

class DecisionOutput(BaseModel):
    selected_route:int
    reason:str
    departure_time:str
    traffic_effect:str
    weather_effect:str
    summary:str

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

structured_llm = llm.with_structured_output(DecisionOutput)

prompt = ChatPromptTemplate.from_messages(
[
(
"system",
"""
You are an intelligent travel planner.

Available Routes

{route}

Traffic

{traffic}

Weather

Choose the best route.

Consider:

• Travel time

• Traffic delay

• Road closures

• Rain

• Overall convenience

Do NOT invent roads.

Choose only from the available routes."""
),
(
"human",
"""
Route:
{route}

Traffic:
{traffic}

Weather:
{weather}
"""
)
])

decision_agent = (
    prompt
    | structured_llm
).with_config(
    {"run_name": "Decision Agent"}
)

def decision_node(state: RouteState):
    start = time.time()
    route_data = state["route"]

    if "error" in route_data:
        raise ValueError(f"Route Tool Error: {route_data['error']}")

    if "routes" not in route_data:
        raise ValueError(f"Unexpected route response: {route_data}")
    route_summary = []

    for r in state["route"]["routes"]:
        route_summary.append({
            "route_id": r["route_id"],
            "distance_km": r["distance_km"],
            "travel_time_min": r["travel_time_min"],
            "traffic_delay_min": r["traffic_delay_min"]
        })

    response = decision_agent.invoke(
    {
        "route": route_summary,
        "traffic": state["traffic"],
        "weather": state["weather"],
    }
    )
    end = time.time()

    print(f"Decision Agent took {end-start:.2f} sec")

    return {
        "decision": response.model_dump()
    }