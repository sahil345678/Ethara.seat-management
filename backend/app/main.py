"""FastAPI application entry point.

Creates the FastAPI application with:
- Lifespan events for startup/shutdown logging
- CORS middleware for frontend communication
- Swagger/OpenAPI documentation metadata
- Global exception handlers
- V1 API router
"""

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import configure_logging, get_settings
from app.middleware.error_handler import register_exception_handlers

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    configure_logging(settings)
    logger.info(
        "Starting %s v%s (debug=%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.DEBUG,
    )
    yield
    logger.info("Shutting down %s", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Health", "description": "Service health and readiness checks"},
        {"name": "Employees", "description": "Employee management operations"},
        {"name": "Projects", "description": "Project management operations"},
        {"name": "Seats", "description": "Seat management and allocation"},
        {"name": "Dashboard", "description": "Analytics and statistics"},
        {"name": "AI Assistant", "description": "Natural language seat and project queries"},
    ],
)

# ── CORS Middleware ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global Exception Handlers ───────────────────────────────────────────────
register_exception_handlers(app)

# ── Routers ─────────────────────────────────────────────────────────────────
app.include_router(v1_router)
