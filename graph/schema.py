# graph/schema.py

from pydantic import BaseModel, Field

class DecisionSchema(BaseModel):
    best_route: str = Field(description="Best route recommendation")
    departure_recommendation: str = Field(description="Leave now or later")
    rain_impact: str = Field(description="Whether rain affects the trip")
    traffic_impact: str = Field(description="Traffic impact on the trip")
    summary: str = Field(description="Overall recommendation")