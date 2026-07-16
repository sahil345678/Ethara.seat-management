"""Employee ORM model.

Employees are the central entity — each employee belongs to one
project and can hold one active seat allocation at a time.

Indexes
-------
- Unique on ``employee_code`` and ``email`` (implicit via unique constraint).
- B-tree on ``project_id`` for FK lookups.
- B-tree on ``status`` for filtered listing.
- GIN trigram on ``name`` for case-insensitive partial-match search
  (requires the ``pg_trgm`` PostgreSQL extension).
"""

import uuid
from datetime import date
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import EmployeeStatus
from app.db.base import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.seat_allocation import SeatAllocation


class Employee(Base, TimestampMixin):
    """Represents an employee at Ethara.

    Columns
    -------
    id : UUID
        Primary key, auto-generated.
    employee_code : str
        Unique human-readable code (e.g., ``ETH-0001``).
    name : str
        Full name.
    email : str
        Unique corporate email.
    department : str | None
        Department name (e.g., Engineering, HR).
    role : str | None
        Job title / role.
    joining_date : date
        Date the employee joined Ethara.
    status : EmployeeStatus
        Active or Inactive.
    project_id : UUID | None
        FK to the assigned project (nullable for unassigned employees).
    created_at, updated_at : datetime
        Timestamps via TimestampMixin.
    """

    __tablename__ = "employees"
    __table_args__ = (
        sa.Index("idx_employee_project", "project_id"),
        sa.Index("idx_employee_status", "status"),
        sa.Index("idx_employee_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        sa.Uuid, primary_key=True, default=uuid.uuid4
    )
    employee_code: Mapped[str] = mapped_column(
        sa.String(20), unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(sa.String(150), nullable=False)
    email: Mapped[str] = mapped_column(
        sa.String(255), unique=True, nullable=False
    )
    department: Mapped[str | None] = mapped_column(
        sa.String(100), nullable=True
    )
    role: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    joining_date: Mapped[date] = mapped_column(sa.Date, nullable=False)
    status: Mapped[EmployeeStatus] = mapped_column(
        sa.Enum(EmployeeStatus, name="employee_status"),
        nullable=False,
        default=EmployeeStatus.ACTIVE,
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.Uuid, sa.ForeignKey("projects.id"), nullable=True
    )

    # ── Relationships ────────────────────────────────────────────────────
    project: Mapped["Project | None"] = relationship(
        back_populates="employees",
    )
    seat_allocations: Mapped[list["SeatAllocation"]] = relationship(
        back_populates="employee",
    )

    def __repr__(self) -> str:
        return (
            f"<Employee(id={self.id}, code='{self.employee_code}', "
            f"name='{self.name}')>"
        )
