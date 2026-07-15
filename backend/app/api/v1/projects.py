"""Projects API routes."""

import math
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.enums import ProjectStatus
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.project_repo import ProjectRepository
from app.schemas import PaginatedResponse, PaginationMeta
from app.schemas.employee import EmployeeResponse
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.employee_service import EmployeeService
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """Dependency injection for ProjectService."""
    return ProjectService(ProjectRepository(db))


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    """Dependency injection for EmployeeService."""
    return EmployeeService(EmployeeRepository(db), ProjectRepository(db))


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
def create_project(
    data: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """Create a new project."""
    return service.create_project(data)


@router.get(
    "",
    response_model=PaginatedResponse[ProjectResponse],
    summary="List projects with filtering and pagination",
)
def get_projects(
    status: ProjectStatus | None = Query(None, description="Filter by status"),
    search: str | None = Query(None, description="Search by name"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("name", description="Field to sort by"),
    sort_desc: bool = Query(False, description="Sort descending"),
    service: ProjectService = Depends(get_project_service),
) -> PaginatedResponse[ProjectResponse]:
    """Retrieve a paginated list of projects."""
    skip = (page - 1) * page_size
    items, total = service.list_projects(
        status=status,
        search=search,
        skip=skip,
        limit=page_size,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    meta = PaginationMeta(
        total=total, page=page, page_size=page_size, total_pages=total_pages
    )
    return PaginatedResponse(data=list(items), meta=meta)


@router.get(
    "/{id}/employees",
    response_model=PaginatedResponse[EmployeeResponse],
    summary="List employees in a specific project",
)
def get_project_employees(
    id: uuid.UUID,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    service: EmployeeService = Depends(get_employee_service),
) -> PaginatedResponse[EmployeeResponse]:
    """Retrieve all employees assigned to a specific project ID."""
    skip = (page - 1) * page_size
    items, total = service.list_employees(project_id=id, skip=skip, limit=page_size)

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    meta = PaginationMeta(
        total=total, page=page, page_size=page_size, total_pages=total_pages
    )
    return PaginatedResponse(data=list(items), meta=meta)
