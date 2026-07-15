"""Pydantic schemas for the Project entity.

Schemas
-------
ProjectCreate   — Validates incoming POST /projects requests.
ProjectUpdate   — Validates incoming PUT /projects/{id} requests (partial).
ProjectBrief    — Lightweight schema for nesting inside other responses.
ProjectResponse — Full response returned by GET endpoints.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import ProjectStatus


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Project name (e.g., Indigo, Talos).",
        examples=["Indigo"],
    )
    description: str | None = Field(
        None,
        max_length=500,
        description="Optional project description.",
    )
    manager_name: str | None = Field(
        None,
        max_length=150,
        description="Name of the project manager.",
    )
    status: ProjectStatus = Field(
        default=ProjectStatus.ACTIVE,
        description="Project status.",
    )


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project.  All fields are optional."""

    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Updated project name.",
    )
    description: str | None = Field(
        None,
        max_length=500,
        description="Updated description.",
    )
    manager_name: str | None = Field(
        None,
        max_length=150,
        description="Updated manager name.",
    )
    status: ProjectStatus | None = Field(
        None,
        description="Updated project status.",
    )


class ProjectBrief(BaseModel):
    """Lightweight project representation for nesting in other responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    status: ProjectStatus


class ProjectResponse(BaseModel):
    """Full project representation returned by API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    manager_name: str | None
    status: ProjectStatus
    created_at: datetime
