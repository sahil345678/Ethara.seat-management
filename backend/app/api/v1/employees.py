"""Employees API routes."""

import math
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.enums import EmployeeStatus
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.project_repo import ProjectRepository
from app.schemas import PaginatedResponse, PaginationMeta
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    """Dependency injection for EmployeeService."""
    return EmployeeService(EmployeeRepository(db), ProjectRepository(db))


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
)
def create_employee(
    data: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    """Create a new employee with the provided details."""
    return service.create_employee(data)


@router.get(
    "",
    response_model=PaginatedResponse[EmployeeResponse],
    summary="List employees with filtering and pagination",
)
def get_employees(
    status: EmployeeStatus | None = Query(None, description="Filter by status"),
    project_id: uuid.UUID | None = Query(None, description="Filter by project"),
    search: str | None = Query(None, description="Search by name, email, or code"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("name", description="Field to sort by"),
    sort_desc: bool = Query(False, description="Sort descending"),
    service: EmployeeService = Depends(get_employee_service),
) -> PaginatedResponse[EmployeeResponse]:
    """Retrieve a paginated list of employees matching the criteria."""
    skip = (page - 1) * page_size
    items, total = service.list_employees(
        status=status,
        project_id=project_id,
        search=search,
        skip=skip,
        limit=page_size,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    return PaginatedResponse(
        data=list(items),
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get(
    "/{id}",
    response_model=EmployeeResponse,
    summary="Get an employee by ID",
)
def get_employee_by_id(
    id: uuid.UUID,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    """Fetch a single employee by their UUID."""
    return service.get_employee(id)


@router.put(
    "/{id}",
    response_model=EmployeeResponse,
    summary="Update an employee",
)
def update_employee(
    id: uuid.UUID,
    data: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    """Update an employee's details. Only provided fields are updated."""
    return service.update_employee(id, data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an employee",
)
def delete_employee(
    id: uuid.UUID,
    service: EmployeeService = Depends(get_employee_service),
) -> None:
    """Delete an employee by their UUID.

    Note: Due to constraints in Phase 6, delete_employee was not added to the
    Service Layer, so we fetch and delete via the underlying repository while
    maintaining the transaction boundary here.
    """
    employee = service.get_employee(id)
    service.repo.delete(employee)
    service.repo.db.commit()
