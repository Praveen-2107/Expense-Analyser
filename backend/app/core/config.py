from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="AI Expense Analyzer")
    app_env: str = Field(default="development")
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    secret_key: str = Field(default="change-me-in-production")
    access_token_expire_minutes: int = Field(default=30)
    jwt_algorithm: str = Field(default="HS256")
    gemini_api_key: str | None = Field(default=None)
    gemini_model: str = Field(default="gemini-1.5-flash")
    uploads_dir: str = Field(default="uploads")
    database_url: str = Field(default="sqlite:///./expense_analyzer.db")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

