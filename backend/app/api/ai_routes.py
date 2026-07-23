from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai.insight_service import generate_ai_insights
from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.ai import AIInsightRequest, AIInsightResponse


ai_router = APIRouter(prefix="/ai", tags=["AI"])


@ai_router.post("/insights", response_model=AIInsightResponse)
def generate_insights(
    request: AIInsightRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, object]:
    return generate_ai_insights(db, current_user, request.focus)

