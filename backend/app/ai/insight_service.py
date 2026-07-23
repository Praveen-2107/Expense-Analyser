from __future__ import annotations

import json
from collections import Counter
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.budget import Budget
from app.models.category import Category
from app.models.expense import Expense
from app.models.income import Income
from app.models.user import User

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency fallback
    genai = None


def _decimal_to_float(value: Decimal | None) -> float:
    return float(value or 0)


def get_financial_snapshot(db: Session, user_id: int) -> dict[str, object]:
    recent_expenses = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .order_by(Expense.expense_date.desc(), Expense.created_at.desc())
        .limit(10)
        .all()
    )
    recent_incomes = (
        db.query(Income)
        .filter(Income.user_id == user_id)
        .order_by(Income.income_date.desc(), Income.created_at.desc())
        .limit(10)
        .all()
    )
    budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
    categories = {category.id: category.name for category in db.query(Category).filter(Category.user_id == user_id).all()}

    total_expenses = sum(_decimal_to_float(expense.amount) for expense in recent_expenses)
    total_income = sum(_decimal_to_float(income.amount) for income in recent_incomes)
    net_cash_flow = total_income - total_expenses

    category_totals: Counter[str] = Counter()
    for expense in recent_expenses:
      category_name = categories.get(expense.category_id, "Uncategorized")
      category_totals[category_name] += _decimal_to_float(expense.amount)

    return {
        "total_expenses": round(total_expenses, 2),
        "total_income": round(total_income, 2),
        "net_cash_flow": round(net_cash_flow, 2),
        "recent_expenses": [
            {
                "title": expense.title,
                "amount": _decimal_to_float(expense.amount),
                "date": expense.expense_date.isoformat(),
                "category_id": expense.category_id,
            }
            for expense in recent_expenses
        ],
        "recent_incomes": [
            {
                "title": income.title,
                "amount": _decimal_to_float(income.amount),
                "date": income.income_date.isoformat(),
                "category_id": income.category_id,
            }
            for income in recent_incomes
        ],
        "budgets": [
            {
                "name": budget.name,
                "limit_amount": _decimal_to_float(budget.limit_amount),
                "spent_amount": _decimal_to_float(budget.spent_amount),
                "alert_threshold": budget.alert_threshold,
                "category_id": budget.category_id,
            }
            for budget in budgets
        ],
        "top_categories": category_totals.most_common(5),
    }


def _build_prompt(user: User, snapshot: dict[str, object], focus: str | None) -> str:
    focus_text = focus.strip() if focus else "overall spending and saving opportunities"
    return (
        f"You are a personal finance assistant for {user.full_name}.\n"
        f"Focus: {focus_text}.\n"
        f"Financial snapshot: {json.dumps(snapshot, ensure_ascii=False)}\n\n"
        "Return STRICT JSON with keys summary, insights, recommendations.\n"
        "summary must be one short paragraph. insights must be a list of 3 concise observations. "
        "recommendations must be a list of 3 practical actions."
    )


def _fallback_response(snapshot: dict[str, object]) -> dict[str, object]:
    total_income = float(snapshot["total_income"])
    total_expenses = float(snapshot["total_expenses"])
    net_cash_flow = float(snapshot["net_cash_flow"])
    top_categories = snapshot.get("top_categories", [])
    top_category_name = top_categories[0][0] if top_categories else "Uncategorized"

    insights = [
        f"Your top spending category is {top_category_name}.",
        f"You earned ${total_income:,.2f} and spent ${total_expenses:,.2f} in the latest activity window.",
        f"Net cash flow is ${net_cash_flow:,.2f}; this is a good place to tighten discretionary spend.",
    ]
    recommendations = [
        "Set a weekly cap for your highest spending category.",
        "Review recurring payments and cancel unused subscriptions.",
        "Move a fixed portion of income into savings immediately after payday.",
    ]
    summary = "The current spending pattern is manageable, but discretionary categories could be trimmed to improve savings."
    return {"summary": summary, "insights": insights, "recommendations": recommendations, "used_gemini": False}


def generate_ai_insights(db: Session, user: User, focus: str | None = None) -> dict[str, object]:
    snapshot = get_financial_snapshot(db, user.id)

    if not settings.gemini_api_key or genai is None:
        return _fallback_response(snapshot)

    try:
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(settings.gemini_model)
        response = model.generate_content(_build_prompt(user, snapshot, focus))
        payload_text = getattr(response, "text", None) or ""
        parsed = json.loads(payload_text)

        summary = str(parsed.get("summary", ""))
        insights = [str(item) for item in parsed.get("insights", [])][:3]
        recommendations = [str(item) for item in parsed.get("recommendations", [])][:3]

        if not summary or not insights or not recommendations:
            raise ValueError("Gemini response missing required fields")

        return {
            "summary": summary,
            "insights": insights,
            "recommendations": recommendations,
            "used_gemini": True,
        }
    except Exception:
        return _fallback_response(snapshot)
