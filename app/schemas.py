from typing import Literal
from pydantic import BaseModel, Field

Goal = Literal["weight loss", "muscle gain", "general wellness", "flexibility", "endurance"]
Intensity = Literal["low", "medium", "high"]

class UserInput(BaseModel):
    user_id: str = Field(min_length=2, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=13, le=100)
    weight_kg: float = Field(gt=25, le=350)
    goal: Goal
    intensity: Intensity

class FeedbackInput(BaseModel):
    user_id: str = Field(min_length=2, max_length=64)
    feedback: str = Field(min_length=5, max_length=1000)
