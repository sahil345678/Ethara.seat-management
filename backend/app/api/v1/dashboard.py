"""Dashboard analytics API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.allocation_repo import AllocationRepository
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.project_repo import ProjectRepository
from app.repositories.seat_repo import SeatRepository
from app.schemas.dashboard import DashboardSummary, FloorUtilization, ProjectUtilization
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    """Dependency injection for DashboardService."""
    return DashboardService(
        employee_repo=EmployeeRepository(db),
        seat_repo=SeatRepository(db),
        allocation_repo=AllocationRepository(db),
        project_repo=ProjectRepository(db),
    )


@router.get(
    "/summary",
    response_model=DashboardSummary,
    summary="Get global dashboard KPIs",
)
def get_summary(
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardSummary:
    """Retrieve top-level statistics (totals, occupancy rate, pending allocations)."""
    return service.get_summary()


@router.get(
    "/project-utilization",
    response_model=list[ProjectUtilization],
    summary="Get seat utilization per project",
)
def get_project_utilization(
    service: DashboardService = Depends(get_dashboard_service),
) -> list[ProjectUtilization]:
    """Retrieve breakdown of active seat allocations by project."""
    return service.get_project_utilization()


@router.get(
    "/floor-utilization",
    response_model=list[FloorUtilization],
    summary="Get seat distribution per floor",
)
def get_floor_utilization(
    service: DashboardService = Depends(get_dashboard_service),
) -> list[FloorUtilization]:
    """Retrieve seat status breakdowns mapped out by physical floors."""
    return service.get_floor_utilization()
