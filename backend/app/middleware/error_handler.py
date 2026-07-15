"""Global exception handlers for the FastAPI application.

Registers handlers that translate domain exceptions, database errors,
and unhandled exceptions into consistent JSON error responses as
defined in the implementation plan (Section 15).

Response format:
    {
        "error": true,
        "code": <http_status_code>,
        "message": "<human-readable message>",
        "detail": "<optional additional detail>"
    }
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError

from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Register all global exception handlers on the FastAPI application."""

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request, exc: AppException
    ) -> JSONResponse:
        """Handle all custom business exceptions."""
        logger.warning(
            "AppException on %s %s — [%d] %s",
            request.method,
            request.url.path,
            exc.status_code,
            exc.message,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "code": exc.status_code,
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
        request: Request, exc: IntegrityError
    ) -> JSONResponse:
        """Handle database constraint violations (unique, FK, etc.)."""
        logger.error(
            "IntegrityError on %s %s — %s",
            request.method,
            request.url.path,
            str(exc.orig),
        )
        return JSONResponse(
            status_code=409,
            content={
                "error": True,
                "code": 409,
                "message": "A database integrity constraint was violated.",
                "detail": str(exc.orig) if exc.orig else None,
            },
        )

    @app.exception_handler(OperationalError)
    async def operational_error_handler(
        request: Request, exc: OperationalError
    ) -> JSONResponse:
        """Handle database connectivity and operational failures."""
        logger.critical(
            "OperationalError on %s %s — %s",
            request.method,
            request.url.path,
            str(exc.orig),
        )
        return JSONResponse(
            status_code=503,
            content={
                "error": True,
                "code": 503,
                "message": "Database service is currently unavailable.",
                "detail": None,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Catch-all for any unhandled exception — prevents stack trace leaks."""
        logger.exception(
            "Unhandled exception on %s %s: %s",
            request.method,
            request.url.path,
            str(exc),
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "code": 500,
                "message": "An internal server error occurred.",
                "detail": None,
            },
        )
