"""Pydantic schemas for dashboard analytics endpoints.

Schemas
-------
DashboardSummary      — GET /dashboard/summary response.
ProjectUtilization    — GET /dashboard/project-utilization list item.
FloorUtilization      — GET /dashboard/floor-utilization list item.
"""

import uuid

from pydantic import BaseModel, Field


class DashboardSummary(BaseModel):
    """Aggregated statistics for the dashboard KPI cards.

    All counts are computed server-side from the database.
    ``occupancy_rate`` is a percentage (0.0 – 100.0).
    """

    total_employees: int = Field(
        ..., description="Total number of employees in the system."
    )
    total_seats: int = Field(
        ..., description="Total number of physical seats."
    )
    occupied_seats: int = Field(
        ..., description="Seats with status 'Occupied'."
    )
    available_seats: int = Field(
        ..., description="Seats with status 'Available'."
    )
    reserved_seats: int = Field(
        ..., description="Seats with status 'Reserved'."
    )
    maintenance_seats: int = Field(
        ..., description="Seats with status 'Maintenance'."
    )
    occupancy_rate: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Percentage of seats occupied (0.0 – 100.0).",
    )
    pending_allocation: int = Field(
        ...,
        description=(
            "Active employees without an active seat allocation."
        ),
    )


class ProjectUtilization(BaseModel):
    """Seat allocation breakdown for a single project.

    Returned as a list by GET /dashboard/project-utilization.
    """

    project_id: uuid.UUID = Field(..., description="UUID of the project.")
    project_name: str = Field(..., description="Project display name.")
    allocated_seats: int = Field(
        ..., description="Number of active seat allocations for this project."
    )
    employee_count: int = Field(
        ..., description="Total employees assigned to this project."
    )


class FloorUtilization(BaseModel):
    """Seat status breakdown for a single floor.

    Returned as a list by GET /dashboard/floor-utilization.
    """

    floor: int = Field(..., description="Floor number.")
    total_seats: int = Field(
        ..., description="Total seats on this floor."
    )
    available: int = Field(..., description="Available seats.")
    occupied: int = Field(..., description="Occupied seats.")
    reserved: int = Field(..., description="Reserved seats.")
    maintenance: int = Field(..., description="Seats under maintenance.")
