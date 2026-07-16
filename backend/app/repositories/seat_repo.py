"""Seat repository for database operations."""

import uuid
from typing import Sequence

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session, selectinload

from app.core.enums import SeatStatus
from app.models.seat import Seat


class SeatRepository:
    """Repository for the Seat entity."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, seat_id: uuid.UUID) -> Seat | None:
        """Fetch a seat by UUID."""
        stmt = select(Seat).where(Seat.id == seat_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_location(
        self, floor: int, zone: str, bay: str, seat_number: str
    ) -> Seat | None:
        """Fetch a seat by its composite unique location attributes."""
        stmt = select(Seat).where(
            Seat.floor == floor,
            Seat.zone == zone,
            Seat.bay == bay,
            Seat.seat_number == seat_number,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_seats(
        self,
        floor: int | None = None,
        zone: str | None = None,
        status: SeatStatus | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "label",
        sort_desc: bool = False,
    ) -> tuple[Sequence[Seat], int]:
        """List seats with filtering, search, sorting, and pagination."""
        stmt = select(Seat).options(
            selectinload(Seat.seat_allocations).selectinload("employee"),
            selectinload(Seat.seat_allocations).selectinload("project")
        )

        if floor is not None:
            stmt = stmt.where(Seat.floor == floor)
        if zone:
            stmt = stmt.where(Seat.zone == zone)
        if status:
            stmt = stmt.where(Seat.status == status)
        if search:
            stmt = stmt.where(Seat.seat_number.ilike(f"%{search}%"))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar_one()

        # Custom sorting logic because `label` is a computed Python property,
        # not a database column. Sort by physical layout hierarchy instead.
        if sort_by == "label" or not hasattr(Seat, sort_by):
            order_cols = [Seat.floor, Seat.zone, Seat.bay, Seat.seat_number]
            if sort_desc:
                stmt = stmt.order_by(*[desc(c) for c in order_cols])
            else:
                stmt = stmt.order_by(*[asc(c) for c in order_cols])
        else:
            sort_col = getattr(Seat, sort_by)
            if sort_desc:
                stmt = stmt.order_by(desc(sort_col))
            else:
                stmt = stmt.order_by(asc(sort_col))

        stmt = stmt.offset(skip).limit(limit)
        items = self.db.execute(stmt).scalars().all()

        return items, total

    def create(self, seat: Seat) -> Seat:
        """Add a new seat to the database."""
        self.db.add(seat)
        self.db.flush()
        return seat

    def update(self, seat: Seat) -> Seat:
        """Update an existing seat in the database."""
        self.db.add(seat)
        self.db.flush()
        return seat

    def delete(self, seat: Seat) -> None:
        """Delete a seat from the database."""
        self.db.delete(seat)
        self.db.flush()
