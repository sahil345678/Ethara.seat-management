"""AI Assistant API route (Placeholder for Phase 14)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.allocation_repo import AllocationRepository
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.project_repo import ProjectRepository
from app.repositories.seat_repo import SeatRepository
from app.schemas.ai import AiQueryRequest, AiQueryResponse
from app.services.ai_service import AiService
from app.services.allocation_service import AllocationService
from app.services.dashboard_service import DashboardService
from app.services.employee_service import EmployeeService
from app.services.project_service import ProjectService
from app.services.seat_service import SeatService

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


def get_ai_service(db: Session = Depends(get_db)) -> AiService:
    """Dependency injection for AiService and its dependent services."""
    emp_repo = EmployeeRepository(db)
    proj_repo = ProjectRepository(db)
    seat_repo = SeatRepository(db)
    alloc_repo = AllocationRepository(db)

    emp_svc = EmployeeService(emp_repo, proj_repo)
    proj_svc = ProjectService(proj_repo)
    seat_svc = SeatService(seat_repo)
    dash_svc = DashboardService(emp_repo, seat_repo, alloc_repo, proj_repo)
    alloc_svc = AllocationService(alloc_repo, seat_repo, emp_repo)

    return AiService(emp_svc, proj_svc, seat_svc, dash_svc, alloc_svc)


@router.post(
    "/query",
    response_model=AiQueryResponse,
    summary="Query the AI assistant",
)
def query_ai_assistant(
    data: AiQueryRequest, service: AiService = Depends(get_ai_service)
) -> AiQueryResponse:
    """Natural language interface for querying the seat allocation system."""
    answer = service.process_query(data.query)
    return AiQueryResponse(answer=answer, data={"query": data.query})
