from fastapi import APIRouter

from app.api.ai_routes import ai_router
from app.api.expense_routes import expense_router
from app.api.income_routes import income_router
from app.api.auth_routes import auth_router
from app.api.upload_routes import upload_router
from app.api.prediction_routes import prediction_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(expense_router)
api_router.include_router(income_router)
api_router.include_router(ai_router)
api_router.include_router(upload_router)
api_router.include_router(prediction_router)


@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


