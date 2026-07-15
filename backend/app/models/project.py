"""Project ORM model.

Projects are the primary grouping mechanism for the seat allocation
algorithm.  Each employee is mapped to one active project, and the
allocator uses project membership to seat teammates together.
"""

import uuid
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ProjectStatus
from app.db.base import Base
from app.models.base import CreatedAtMixin

if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.seat_allocation import SeatAllocation


class Project(Base, CreatedAtMixin):
    """Represents a project that employees are assigned to.

    Columns
    -------
    id : UUID
        Primary key, auto-generated.
    name : str
        Project name (e.g., Indigo, Indreed, Talos).
    description : str | None
        Optional project description.
    manager_name : str | None
        Name of the project manager.
    status : ProjectStatus
        Active or Completed.
    created_at : datetime
        Timestamp of record creation (via CreatedAtMixin).
    """

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        sa.Uuid, primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    manager_name: Mapped[str | None] = mapped_column(
        sa.String(150), nullable=True
    )
    status: Mapped[ProjectStatus] = mapped_column(
        sa.Enum(ProjectStatus, name="project_status"),
        nullable=False,
        default=ProjectStatus.ACTIVE,
    )

    # ── Relationships ────────────────────────────────────────────────────
    employees: Mapped[list["Employee"]] = relationship(
        back_populates="project",
    )
    seat_allocations: Mapped[list["SeatAllocation"]] = relationship(
        back_populates="project",
    )

    def __repr__(self) -> str:
        return (
            f"<Project(id={self.id}, name='{self.name}', "
            f"status='{self.status.value}')>"
        )
