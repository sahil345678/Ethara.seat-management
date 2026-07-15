"""Pydantic schemas for seat allocation and release operations.

Schemas
-------
SeatAllocateRequest      — POST /seats/allocate request body.
SeatReleaseRequest       — POST /seats/release request body.
SeatAllocationResponse   — Full allocation record with nested briefs.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.enums import AllocationStatus
from app.schemas.employee import EmployeeBrief
from app.schemas.project import ProjectBrief
from app.schemas.seat import SeatBrief


class SeatAllocateRequest(BaseModel):
    """Request body for allocating a seat to an employee.

    If ``seat_id`` is provided, the system performs a **manual allocation**
    to that specific seat.  If ``seat_id`` is omitted (None), the system
    runs the **auto-allocation algorithm** to find the best available seat
    based on project-team proximity.
    """

    employee_id: uuid.UUID = Field(
        ...,
        description="UUID of the employee to allocate a seat for.",
    )
    seat_id: uuid.UUID | None = Field(
        None,
        description=(
            "UUID of the specific seat to allocate. "
            "Omit for auto-allocation based on team proximity."
        ),
    )


class SeatReleaseRequest(BaseModel):
    """Request body for releasing an active seat allocation.

    At least one of ``employee_id`` or ``seat_id`` must be provided.
    The system will find and release the active allocation matching
    the given identifier.
    """

    employee_id: uuid.UUID | None = Field(
        None,
        description="UUID of the employee whose seat should be released.",
    )
    seat_id: uuid.UUID | None = Field(
        None,
        description="UUID of the seat to release.",
    )

    @model_validator(mode="after")
    def validate_at_least_one_identifier(self) -> "SeatReleaseRequest":
        """Ensure at least one identifier is provided."""
        if self.employee_id is None and self.seat_id is None:
            raise ValueError(
                "At least one of 'employee_id' or 'seat_id' must be provided."
            )
        return self


class SeatAllocationResponse(BaseModel):
    """Full seat allocation record returned by API responses.

    Includes nested brief schemas for the employee, seat, and project
    when the corresponding ORM relationships are loaded.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    employee_id: uuid.UUID
    seat_id: uuid.UUID
    project_id: uuid.UUID
    allocation_status: AllocationStatus
    allocation_date: datetime
    released_date: datetime | None
    employee: EmployeeBrief | None = None
    seat: SeatBrief | None = None
    project: ProjectBrief | None = None
