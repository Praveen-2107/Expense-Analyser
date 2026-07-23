from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app import models  # noqa: F401
from app.api.routes import api_router
from app.core.config import settings
from app.database.session import Base, engine


app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    Path(settings.uploads_dir).mkdir(parents=True, exist_ok=True)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} API is running"}


