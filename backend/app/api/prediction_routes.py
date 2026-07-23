from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.prediction import ExpenseForecastResponse, ForecastRequest
from app.services.prediction_service import predict_expense_forecast


prediction_router = APIRouter(prefix="/predictions", tags=["Predictions"])


@prediction_router.post("/expense-forecast", response_model=ExpenseForecastResponse)
def expense_forecast(
    request: ForecastRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, object]:
    return predict_expense_forecast(db, current_user.id, request)

