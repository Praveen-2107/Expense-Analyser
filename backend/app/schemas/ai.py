from pydantic import BaseModel, Field


class AIInsightRequest(BaseModel):
    focus: str | None = Field(default=None, max_length=200)


class AIInsightResponse(BaseModel):
    summary: str
    insights: list[str]
    recommendations: list[str]
    used_gemini: bool

