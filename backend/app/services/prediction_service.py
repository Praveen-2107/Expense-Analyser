from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

import pandas as pd
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.prediction import ForecastRequest


def _to_float(value: Decimal | None) -> float:
    return float(value or 0)


def _build_monthly_series(db: Session, user_id: int) -> pd.Series:
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    if not expenses:
        return pd.Series(dtype=float)

    frame = pd.DataFrame(
        {
            "expense_date": [expense.expense_date for expense in expenses],
            "amount": [_to_float(expense.amount) for expense in expenses],
        }
    )
    frame["expense_date"] = pd.to_datetime(frame["expense_date"])
    monthly = frame.set_index("expense_date").resample("MS").sum().fillna(0.0)["amount"]
    return monthly


def _predict_with_linear_regression(monthly_series: pd.Series, months_ahead: int) -> list[float]:
    x_values = pd.RangeIndex(start=0, stop=len(monthly_series)).to_numpy().reshape(-1, 1)
    y_values = monthly_series.to_numpy(dtype=float)

    model = LinearRegression()
    model.fit(x_values, y_values)

    future_indexes = pd.RangeIndex(start=len(monthly_series), stop=len(monthly_series) + months_ahead).to_numpy().reshape(-1, 1)
    predictions = model.predict(future_indexes)
    return [max(round(float(value), 2), 0.0) for value in predictions]


def _predict_with_moving_average(monthly_series: pd.Series, months_ahead: int) -> list[float]:
    window = monthly_series.tail(3) if len(monthly_series) >= 3 else monthly_series
    average = float(window.mean()) if not window.empty else 0.0
    return [max(round(average, 2), 0.0) for _ in range(months_ahead)]


def _next_month_start(reference: pd.Timestamp | None) -> pd.Timestamp:
    if reference is None:
        reference = pd.Timestamp(datetime.utcnow().date())
    reference = reference.to_period("M").to_timestamp(how="start")
    return reference + pd.offsets.MonthBegin(1)


def predict_expense_forecast(db: Session, user_id: int, request: ForecastRequest) -> dict[str, object]:
    monthly_series = _build_monthly_series(db, user_id)

    if monthly_series.empty:
        forecast_values = [0.0 for _ in range(request.months_ahead)]
        return {
            "model_name": "expense_forecast",
            "training_points": 0,
            "last_month_actual": None,
            "next_month_prediction": 0.0,
            "forecast": [
                {"month": (_next_month_start(None) + pd.DateOffset(months=index)).date(), "predicted_expense": 0.0}
                for index in range(request.months_ahead)
            ],
            "method": "no_history",
            "confidence": "low",
            "message": "No expense history available yet. Add more expense transactions to generate a forecast.",
        }

    months_ahead = request.months_ahead
    last_month_actual = float(monthly_series.iloc[-1])

    if len(monthly_series) >= 3:
        forecast_values = _predict_with_linear_regression(monthly_series, months_ahead)
        method = "linear_regression"
        confidence = "medium" if len(monthly_series) < 6 else "high"
        message = "Forecast generated from monthly expense history using a regression model."
    else:
        forecast_values = _predict_with_moving_average(monthly_series, months_ahead)
        method = "moving_average"
        confidence = "low"
        message = "Not enough monthly data for regression, so a moving average fallback was used."

    last_period = monthly_series.index[-1]
    next_month_start = _next_month_start(pd.Timestamp(last_period))
    forecast = []
    for index, value in enumerate(forecast_values):
        forecast_month = next_month_start + pd.DateOffset(months=index)
        forecast.append({"month": forecast_month.date(), "predicted_expense": value})

    return {
        "model_name": "expense_forecast",
        "training_points": len(monthly_series),
        "last_month_actual": round(last_month_actual, 2),
        "next_month_prediction": forecast_values[0],
        "forecast": forecast,
        "method": method,
        "confidence": confidence,
        "message": message,
    }
