import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from graph.state import RouteState

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)
def report_node(state:RouteState):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
            You are an expert AI Travel Report Generator.

Generate ONLY the final travel report.

Do NOT explain your reasoning.
Do NOT write phrases like:
- "Based on the provided information"
- "I think"
- "It appears"

Write the report in professional Markdown.

-----------------------------------------
RULES
-----------------------------------------

1. Journey Overview
Include:
• Source
• Destination
• Distance (km)
• Estimated Travel Time (convert minutes into hours and minutes)

2. Traffic Analysis
• Mention only traffic affecting the selected route.
• If nearby incidents do not affect the route, say:

'No significant traffic congestion is expected on the selected route.'

• Mention the traffic delay only if it is greater than zero.

3. Weather Analysis
• Describe only the weather during the journey.
• Ignore weather occurring after the estimated arrival time.
• If rain is not expected during travel, say:

'No rainfall is expected during the journey.'

• Mention temperature in a friendly format.

4. Departure Recommendation
Convert timestamps into readable local time.

Example:

Leave at approximately 3:45 PM.

Expected arrival: 4:08 PM.

Never display ISO timestamps.

Never display seconds.

5. Journey Status

Generate one status:

🟢 Excellent time to travel

🟡 Minor delays expected

🔴 Consider delaying your trip

Choose based on traffic and weather.

6. Final Recommendation

Provide 3 concise bullet points.

Example:

✅ Leave now

• Route is clear.
• Weather is favorable.
• No significant delays expected.

7. Summary

Summarize in no more than three sentences.

Do not repeat previous sections.

-----------------------------------------

Use this exact structure.

 🚗 AI Travel Report

 🟢 Journey Status

 🚗 Journey Overview

 🚦 Traffic Analysis

 🌤 Weather Analysis

 🕒 Departure Recommendation

 ✅ Final Recommendation

 📌 Summary
        """
            ),
            (
                "human",
                """
    Source:
    {source}

    Destination:
    {destination}

    Departure Recommendation:
    {departure}

    Traffic Analysis:
    {traffic_effect}

    Weather Analysis:
    {weather_effect}

    Selected Route:
    {chosen_route}

    Traffic Summary:
    {traffic}

    Weather Summary:
    {weather}
    """
            )
        ]
    )

    report_agent = (prompt | llm).with_config(
    {"run_name": "Report Generator"}
)

    decision = state["decision"]
    selected = decision["selected_route"]
    chosen_route = state["route"]["routes"][selected-1]

    chosen_route_summary = {
    "distance_km": chosen_route["distance_km"],
    "travel_time_min": chosen_route["travel_time_min"],
    "traffic_delay_min": chosen_route["traffic_delay_min"],
    "departure_time": chosen_route["departure_time"],
    "arrival_time": chosen_route["arrival_time"]
    }

    traffic_summary = {
    "incident_count": len(state["traffic"].get("incidents", [])),
    "delay": decision["traffic_effect"]
    }

    weather_summary = {
    "condition": decision["weather_effect"]
    }

    print("Decision:", decision)
    print(type(decision))
    response = report_agent.invoke({
        "source": state["source"],
        "destination": state["destination"],
        "chosen_route": chosen_route_summary,
        "departure": decision["departure_time"],
        "traffic_effect": decision["traffic_effect"],
        "weather_effect": decision["weather_effect"],
        "traffic": traffic_summary,
        "weather": weather_summary
        })
    
    os.makedirs("reports", exist_ok=True)

    # Save latest report
    with open("reports/latest_report.txt", "w", encoding="utf-8") as f:
        f.write(response.content)

    # Save timestamped report
    filename = datetime.now().strftime(
        "reports/report_%Y%m%d_%H%M%S.md"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.content)

    return {
        "report": response.content
    }