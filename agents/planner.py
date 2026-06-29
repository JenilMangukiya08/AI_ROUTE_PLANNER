from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from typing import TypedDict
load_dotenv()

class PlannerOutput(TypedDict):
    source: str
    destination: str


def planner_node(state):
    return {
        "source": state["source"],
        "destination": state["destination"]
    }

class Location(BaseModel):
    source: str
    destination: str


llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

structured_llm = llm.with_structured_output(Location)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Extract only the source and destination.

            Return nothing except the structured output.
            """
        ),
        ("human", "{query}")
    ]
)


planner = (prompt | structured_llm).with_config(
    {"run_name": "Planner Agent"}
)