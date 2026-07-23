from fastapi import APIRouter

from app.api.auth_routes import auth_router


api_router = APIRouter()
api_router.include_router(auth_router)


@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


