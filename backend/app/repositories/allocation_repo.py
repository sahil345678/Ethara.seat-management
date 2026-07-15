"""SeatAllocation repository for database operations."""

import uuid
from typing import Sequence

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import AllocationStatus
from app.models.seat_allocation import SeatAllocation


class AllocationRepository:
    """Repository for the SeatAllocation entity."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, allocation_id: uuid.UUID) -> SeatAllocation | None:
        """Fetch an allocation by UUID, eagerly loading associated entities."""
        stmt = (
            select(SeatAllocation)
            .where(SeatAllocation.id == allocation_id)
            .options(
                joinedload(SeatAllocation.employee),
                joinedload(SeatAllocation.seat),
                joinedload(SeatAllocation.project),
            )
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_active_for_employee(
        self, employee_id: uuid.UUID
    ) -> SeatAllocation | None:
        """Fetch the single active seat allocation for an employee."""
        stmt = select(SeatAllocation).where(
            SeatAllocation.employee_id == employee_id,
            SeatAllocation.allocation_status == AllocationStatus.ACTIVE,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_active_for_seat(self, seat_id: uuid.UUID) -> SeatAllocation | None:
        """Fetch the single active seat allocation for a seat."""
        stmt = select(SeatAllocation).where(
            SeatAllocation.seat_id == seat_id,
            SeatAllocation.allocation_status == AllocationStatus.ACTIVE,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_allocations(
        self,
        employee_id: uuid.UUID | None = None,
        seat_id: uuid.UUID | None = None,
        project_id: uuid.UUID | None = None,
        status: AllocationStatus | None = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "allocation_date",
        sort_desc: bool = True,
    ) -> tuple[Sequence[SeatAllocation], int]:
        """List allocations with filtering, sorting, and pagination."""
        stmt = select(SeatAllocation)

        if employee_id:
            stmt = stmt.where(SeatAllocation.employee_id == employee_id)
        if seat_id:
            stmt = stmt.where(SeatAllocation.seat_id == seat_id)
        if project_id:
            stmt = stmt.where(SeatAllocation.project_id == project_id)
        if status:
            stmt = stmt.where(SeatAllocation.allocation_status == status)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar_one()

        sort_col = getattr(
            SeatAllocation, sort_by, SeatAllocation.allocation_date
        )
        if sort_desc:
            stmt = stmt.order_by(desc(sort_col))
        else:
            stmt = stmt.order_by(asc(sort_col))

        # Eager load the related entities for the Response schema
        stmt = (
            stmt.options(
                joinedload(SeatAllocation.employee),
                joinedload(SeatAllocation.seat),
                joinedload(SeatAllocation.project),
            )
            .offset(skip)
            .limit(limit)
        )
        items = self.db.execute(stmt).scalars().all()

        return items, total

    def create(self, allocation: SeatAllocation) -> SeatAllocation:
        """Add a new seat allocation to the database."""
        self.db.add(allocation)
        self.db.flush()
        return allocation

    def update(self, allocation: SeatAllocation) -> SeatAllocation:
        """Update an existing seat allocation in the database."""
        self.db.add(allocation)
        self.db.flush()
        return allocation
