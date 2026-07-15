"""Application configuration using Pydantic Settings.

All settings are loaded from environment variables or a `.env` file.
The Settings instance is cached via `get_settings()` for reuse across
the application without repeated file I/O.
"""

import logging
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # ── Application ──────────────────────────────────────────────────────
    APP_NAME: str = "Ethara Seat Allocation & Project Mapping System"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "A centralized system for managing employee seat allocation "
        "and project mapping at Ethara."
    )
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # ── Database (PostgreSQL) ────────────────────────────────────────────
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ethara_db"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # ── CORS ─────────────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # ── AI / Google Gemini ───────────────────────────────────────────────
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-pro"


@lru_cache
def get_settings() -> Settings:
    """Return a cached application settings instance."""
    return Settings()


def configure_logging(settings: Settings) -> None:
    """Configure root logger format and level based on application settings.

    Suppresses noisy third-party loggers to WARNING level so that
    application logs remain readable during development and production.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Suppress noisy third-party loggers
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
