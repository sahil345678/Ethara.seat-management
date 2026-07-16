"""Pydantic schema definitions — public API.

This module exports all entity schemas and provides shared
pagination types used across multiple API endpoints.

Common Schemas
--------------
PaginationMeta      — Metadata for paginated list responses.
PaginatedResponse   — Generic wrapper: ``{ data: [...], meta: {...} }``.

Usage in route handlers::

    from app.schemas import PaginatedResponse, EmployeeResponse

    @router.get("/employees", response_model=PaginatedResponse[EmployeeResponse])
    def list_employees(...):
        ...
"""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

# ── Generic pagination types ────────────────────────────────────────────────

DataT = TypeVar("DataT")


class PaginationMeta(BaseModel):
    """Metadata describing the current page of a paginated result set."""

    total: int = Field(..., description="Total number of matching records.")
    page: int = Field(..., description="Current page number (1-indexed).")
    page_size: int = Field(..., description="Number of records per page.")
    total_pages: int = Field(..., description="Total number of pages.")


class PaginatedResponse(BaseModel, Generic[DataT]):
    """Generic paginated response wrapper.

    Used as ``PaginatedResponse[EmployeeResponse]``,
    ``PaginatedResponse[SeatResponse]``, etc.
    """

    data: list[DataT] = Field(..., description="Page of result records.")
    total: int = Field(..., description="Total number of matching records.")
    page: int = Field(..., description="Current page number (1-indexed).")
    page_size: int = Field(..., description="Number of records per page.")
    total_pages: int = Field(..., description="Total number of pages.")


# ── Entity schema re-exports ────────────────────────────────────────────────

from app.schemas.ai import AiQueryRequest, AiQueryResponse  # noqa: E402
from app.schemas.dashboard import (  # noqa: E402
    DashboardSummary,
    FloorUtilization,
    ProjectUtilization,
)
from app.schemas.employee import (  # noqa: E402
    EmployeeBrief,
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.schemas.project import (  # noqa: E402
    ProjectBrief,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.schemas.seat import (  # noqa: E402
    SeatBrief,
    SeatCreate,
    SeatResponse,
    SeatUpdate,
)
from app.schemas.seat_allocation import (  # noqa: E402
    SeatAllocateRequest,
    SeatAllocationResponse,
    SeatReleaseRequest,
)

__all__ = [
    # Pagination
    "PaginationMeta",
    "PaginatedResponse",
    # AI
    "AiQueryRequest",
    "AiQueryResponse",
    # Dashboard
    "DashboardSummary",
    "FloorUtilization",
    "ProjectUtilization",
    # Employee
    "EmployeeBrief",
    "EmployeeCreate",
    "EmployeeResponse",
    "EmployeeUpdate",
    # Project
    "ProjectBrief",
    "ProjectCreate",
    "ProjectResponse",
    "ProjectUpdate",
    # Seat
    "SeatBrief",
    "SeatCreate",
    "SeatResponse",
    "SeatUpdate",
    # Seat Allocation
    "SeatAllocateRequest",
    "SeatAllocationResponse",
    "SeatReleaseRequest",
]
