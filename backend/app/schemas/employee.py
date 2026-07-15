"""Pydantic schemas for the Employee entity.

Schemas
-------
EmployeeCreate   — Validates incoming POST /employees requests.
EmployeeUpdate   — Validates incoming PUT /employees/{id} requests (partial).
EmployeeBrief    — Lightweight schema for nesting inside other responses.
EmployeeResponse — Full response with optional nested ProjectBrief.
"""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import EmployeeStatus
from app.schemas.project import ProjectBrief


class EmployeeCreate(BaseModel):
    """Schema for creating a new employee."""

    employee_code: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Unique employee identifier (e.g., ETH-0001).",
        examples=["ETH-0001"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Full name of the employee.",
        examples=["Amit Sharma"],
    )
    email: EmailStr = Field(
        ...,
        description="Corporate email address (must be unique).",
        examples=["amit.sharma@ethara.ai"],
    )
    department: str | None = Field(
        None,
        max_length=100,
        description="Department name.",
        examples=["Engineering"],
    )
    role: str | None = Field(
        None,
        max_length=100,
        description="Job title or role.",
        examples=["Software Engineer"],
    )
    joining_date: date = Field(
        ...,
        description="Date the employee joined Ethara.",
        examples=["2025-06-15"],
    )
    status: EmployeeStatus = Field(
        default=EmployeeStatus.ACTIVE,
        description="Employment status.",
    )
    project_id: uuid.UUID | None = Field(
        None,
        description="UUID of the assigned project (None if unassigned).",
    )


class EmployeeUpdate(BaseModel):
    """Schema for updating an existing employee.  All fields are optional.

    Use ``model_dump(exclude_unset=True)`` in the service layer to apply
    only the fields that were explicitly provided in the request body.
    """

    name: str | None = Field(None, min_length=1, max_length=150)
    email: EmailStr | None = Field(None)
    department: str | None = Field(None, max_length=100)
    role: str | None = Field(None, max_length=100)
    joining_date: date | None = Field(None)
    status: EmployeeStatus | None = Field(None)
    project_id: uuid.UUID | None = Field(None)


class EmployeeBrief(BaseModel):
    """Lightweight employee representation for nesting in other responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    employee_code: str
    name: str
    email: str


class EmployeeResponse(BaseModel):
    """Full employee representation returned by API responses.

    The ``project`` field is populated when the ORM relationship is loaded,
    providing the project's name and status without a second API call.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    employee_code: str
    name: str
    email: str
    department: str | None
    role: str | None
    joining_date: date
    status: EmployeeStatus
    project_id: uuid.UUID | None
    project: ProjectBrief | None = None
    created_at: datetime
    updated_at: datetime
