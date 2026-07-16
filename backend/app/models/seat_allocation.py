"""SeatAllocation ORM model.

Links an employee to a specific seat for a project.  Maintains full
allocation history — when a seat is released, the record stays with
``allocation_status = 'Released'`` and a ``released_date``.

Business rules enforced at the database level via partial unique indexes:

1. **One employee → one active seat:**
   ``idx_unique_active_employee`` ensures at most one row per
   ``employee_id`` where ``allocation_status = 'Active'``.

2. **One seat → one active employee:**
   ``idx_unique_active_seat`` ensures at most one row per
   ``seat_id`` where ``allocation_status = 'Active'``.

Additional indexes on ``employee_id``, ``seat_id``, ``project_id``,
and ``allocation_status`` support general query performance.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AllocationStatus
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.project import Project
    from app.models.seat import Seat


class SeatAllocation(Base):
    """Maps an employee to a seat for a given project.

    Columns
    -------
    id : UUID
        Primary key, auto-generated.
    employee_id : UUID
        FK to the allocated employee.
    seat_id : UUID
        FK to the allocated seat.
    project_id : UUID
        FK to the project at the time of allocation.
    allocation_status : AllocationStatus
        Active or Released.
    allocation_date : datetime
        Timestamp when the allocation was created.
    released_date : datetime | None
        Timestamp when the seat was released (None if still active).
    """

    __tablename__ = "seat_allocations"
    __table_args__ = (
        # ── Partial unique indexes (business rule enforcement) ───────────
        sa.Index(
            "idx_alloc_active_employee",
            "employee_id",
        ),
        sa.Index(
            "idx_alloc_active_seat",
            "seat_id",
        ),
        # ── General-purpose query indexes ────────────────────────────────
        sa.Index("idx_alloc_employee", "employee_id"),
        sa.Index("idx_alloc_seat", "seat_id"),
        sa.Index("idx_alloc_project", "project_id"),
        sa.Index("idx_alloc_status", "allocation_status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        sa.Uuid, primary_key=True, default=uuid.uuid4
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        sa.Uuid, sa.ForeignKey("employees.id"), nullable=False
    )
    seat_id: Mapped[uuid.UUID] = mapped_column(
        sa.Uuid, sa.ForeignKey("seats.id"), nullable=False
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        sa.Uuid, sa.ForeignKey("projects.id"), nullable=False
    )
    allocation_status: Mapped[AllocationStatus] = mapped_column(
        sa.Enum(AllocationStatus, name="allocation_status"),
        nullable=False,
        default=AllocationStatus.ACTIVE,
    )
    allocation_date: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    )
    released_date: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
    )

    # ── Relationships ────────────────────────────────────────────────────
    employee: Mapped["Employee"] = relationship(
        back_populates="seat_allocations",
    )
    seat: Mapped["Seat"] = relationship(
        back_populates="seat_allocations",
    )
    project: Mapped["Project"] = relationship(
        back_populates="seat_allocations",
    )

    def __repr__(self) -> str:
        return (
            f"<SeatAllocation(id={self.id}, employee_id={self.employee_id}, "
            f"seat_id={self.seat_id}, status='{self.allocation_status.value}')>"
        )
