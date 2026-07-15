"""V1 API router — aggregates all domain routers under the /api/v1 prefix.

Individual domain routers (employees, projects, seats, dashboard, ai)
will be included here as they are implemented in their respective phases.
"""

from fastapi import APIRouter

from app.api.v1 import ai_assistant, dashboard, employees, projects, seats
from app.core.config import get_settings

settings = get_settings()

router = APIRouter(prefix="/api/v1")

router.include_router(employees.router)
router.include_router(projects.router)
router.include_router(seats.router)
router.include_router(dashboard.router)
router.include_router(ai_assistant.router)

@router.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    response_description="Service health status",
)
async def health_check() -> dict:
    """Return the current health status of the API service.

    This endpoint is used by load balancers, monitoring tools, and
    deployment platforms to verify that the service is operational.
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
