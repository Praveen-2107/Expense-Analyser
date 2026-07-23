from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ForecastRequest(BaseModel):
    months_ahead: int = Field(default=3, ge=1, le=12)


class MonthlyForecastItem(BaseModel):
    month: date
    predicted_expense: float


class ExpenseForecastResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    model_name: str
    training_points: int
    last_month_actual: float | None
    next_month_prediction: float
    forecast: list[MonthlyForecastItem]
    method: str
    confidence: str
    message: str

