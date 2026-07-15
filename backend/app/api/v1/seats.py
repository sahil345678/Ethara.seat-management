"""Seats API routes."""

import math

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.enums import SeatStatus
from app.repositories.allocation_repo import AllocationRepository
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.seat_repo import SeatRepository
from app.schemas import PaginatedResponse, PaginationMeta
from app.schemas.seat import SeatCreate, SeatResponse
from app.schemas.seat_allocation import (
    SeatAllocateRequest,
    SeatAllocationResponse,
    SeatReleaseRequest,
)
from app.services.allocation_service import AllocationService
from app.services.seat_service import SeatService

router = APIRouter(prefix="/seats", tags=["Seats & Allocation"])


def get_seat_service(db: Session = Depends(get_db)) -> SeatService:
    """Dependency injection for SeatService."""
    return SeatService(SeatRepository(db))


def get_allocation_service(db: Session = Depends(get_db)) -> AllocationService:
    """Dependency injection for AllocationService."""
    return AllocationService(
        AllocationRepository(db), SeatRepository(db), EmployeeRepository(db)
    )


@router.post(
    "",
    response_model=SeatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new physical seat",
)
def create_seat(
    data: SeatCreate, service: SeatService = Depends(get_seat_service)
) -> SeatResponse:
    """Add a new physical seat to the office map."""
    return service.create_seat(data)


@router.get(
    "",
    response_model=PaginatedResponse[SeatResponse],
    summary="List all seats",
)
def get_seats(
    floor: int | None = Query(None, description="Filter by floor"),
    zone: str | None = Query(None, description="Filter by zone"),
    status: SeatStatus | None = Query(None, description="Filter by status"),
    search: str | None = Query(None, description="Search by seat number"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("label", description="Field to sort by"),
    sort_desc: bool = Query(False, description="Sort descending"),
    service: SeatService = Depends(get_seat_service),
) -> PaginatedResponse[SeatResponse]:
    """Retrieve a paginated list of all seats."""
    skip = (page - 1) * page_size
    items, total = service.list_seats(
        floor=floor,
        zone=zone,
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
    "/available",
    response_model=PaginatedResponse[SeatResponse],
    summary="List only available seats",
)
def get_available_seats(
    floor: int | None = Query(None, description="Filter by floor"),
    zone: str | None = Query(None, description="Filter by zone"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    service: SeatService = Depends(get_seat_service),
) -> PaginatedResponse[SeatResponse]:
    """Convenience endpoint to retrieve only available seats."""
    skip = (page - 1) * page_size
    items, total = service.list_seats(
        floor=floor,
        zone=zone,
        status=SeatStatus.AVAILABLE,
        skip=skip,
        limit=page_size,
        sort_by="label",
        sort_desc=False,
    )

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    meta = PaginationMeta(
        total=total, page=page, page_size=page_size, total_pages=total_pages
    )
    return PaginatedResponse(data=list(items), meta=meta)


@router.post(
    "/allocate",
    response_model=SeatAllocationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Allocate a seat to an employee",
)
def allocate_seat(
    data: SeatAllocateRequest,
    service: AllocationService = Depends(get_allocation_service),
) -> SeatAllocationResponse:
    """Allocate a seat. If `seat_id` is omitted, auto-allocates based on team proximity."""
    return service.allocate_seat(data)


@router.post(
    "/release",
    response_model=SeatAllocationResponse,
    summary="Release an active seat allocation",
)
def release_seat(
    data: SeatReleaseRequest,
    service: AllocationService = Depends(get_allocation_service),
) -> SeatAllocationResponse:
    """Release a seat by providing either the `employee_id` or `seat_id`."""
    return service.release_seat(employee_id=data.employee_id, seat_id=data.seat_id)
