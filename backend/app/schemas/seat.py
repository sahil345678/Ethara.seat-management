"""Pydantic schemas for the Seat entity.

Schemas
-------
SeatCreate   — Validates incoming POST /seats requests.
SeatUpdate   — Validates incoming PUT requests (primarily status changes).
SeatBrief    — Lightweight schema with label for nesting in allocations.
SeatResponse — Full response including the computed label property.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import SeatStatus


class SeatCreate(BaseModel):
    """Schema for creating a new seat."""

    floor: int = Field(
        ...,
        ge=1,
        description="Floor number (starting from 1).",
        examples=[2],
    )
    zone: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Zone identifier within the floor (e.g., A, B).",
        examples=["B"],
    )
    bay: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Bay identifier within the zone (e.g., 4).",
        examples=["4"],
    )
    seat_number: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Individual seat identifier (e.g., B4-23).",
        examples=["B4-23"],
    )
    status: SeatStatus = Field(
        default=SeatStatus.AVAILABLE,
        description="Initial seat status.",
    )


class SeatUpdate(BaseModel):
    """Schema for updating an existing seat.  All fields are optional."""

    floor: int | None = Field(None, ge=1, description="Updated floor number.")
    zone: str | None = Field(None, min_length=1, max_length=10)
    bay: str | None = Field(None, min_length=1, max_length=10)
    seat_number: str | None = Field(None, min_length=1, max_length=20)
    status: SeatStatus | None = Field(None, description="Updated seat status.")


class SeatBrief(BaseModel):
    """Lightweight seat representation for nesting in allocation responses.

    Includes the computed ``label`` property (e.g., ``F2-ZB-B4-B4-23``)
    from the Seat ORM model.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    floor: int
    zone: str
    bay: str
    seat_number: str
    status: SeatStatus
    label: str


class SeatResponse(BaseModel):
    """Full seat representation returned by API responses.

    The ``label`` field is a computed property on the ORM model
    (e.g., ``F2-ZB-B4-B4-23``), automatically read by Pydantic
    via ``from_attributes=True``.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    floor: int
    zone: str
    bay: str
    seat_number: str
    status: SeatStatus
    label: str
    created_at: datetime
    occupant_name: str | None = None
    project_name: str | None = None
