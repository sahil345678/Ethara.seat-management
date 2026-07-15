"""Seat ORM model.

Seats are organized hierarchically: Floor → Zone → Bay → Seat Number.
A composite unique constraint on ``(floor, zone, bay, seat_number)``
prevents duplicate seat entries within the same physical location.

Indexes
-------
- Composite unique on ``(floor, zone, bay, seat_number)`` via ``uq_seat_location``.
- B-tree on ``status`` for filtering by availability.
- Composite B-tree on ``(floor, zone)`` for floor/zone drill-down queries.
"""

import uuid
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import SeatStatus
from app.db.base import Base
from app.models.base import CreatedAtMixin

if TYPE_CHECKING:
    from app.models.seat_allocation import SeatAllocation


class Seat(Base, CreatedAtMixin):
    """Represents a physical seat in the Ethara office.

    Columns
    -------
    id : UUID
        Primary key, auto-generated.
    floor : int
        Floor number (e.g., 1, 2, 3).
    zone : str
        Zone identifier within the floor (e.g., ``A``, ``B``).
    bay : str
        Bay identifier within the zone (e.g., ``1``, ``4``).
    seat_number : str
        Individual seat identifier (e.g., ``B4-23``).
    status : SeatStatus
        Available, Occupied, Reserved, or Maintenance.
    created_at : datetime
        Timestamp of record creation (via CreatedAtMixin).
    """

    __tablename__ = "seats"
    __table_args__ = (
        sa.UniqueConstraint(
            "floor", "zone", "bay", "seat_number",
            name="uq_seat_location",
        ),
        sa.Index("idx_seat_status", "status"),
        sa.Index("idx_seat_floor_zone", "floor", "zone"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        sa.Uuid, primary_key=True, default=uuid.uuid4
    )
    floor: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    zone: Mapped[str] = mapped_column(sa.String(10), nullable=False)
    bay: Mapped[str] = mapped_column(sa.String(10), nullable=False)
    seat_number: Mapped[str] = mapped_column(sa.String(20), nullable=False)
    status: Mapped[SeatStatus] = mapped_column(
        sa.Enum(SeatStatus, name="seat_status"),
        nullable=False,
        default=SeatStatus.AVAILABLE,
    )

    # ── Relationships ────────────────────────────────────────────────────
    seat_allocations: Mapped[list["SeatAllocation"]] = relationship(
        back_populates="seat",
    )

    @property
    def label(self) -> str:
        """Human-readable seat identifier (e.g., ``F2-ZB-B4-S23``)."""
        return f"F{self.floor}-Z{self.zone}-B{self.bay}-{self.seat_number}"

    def __repr__(self) -> str:
        return (
            f"<Seat(id={self.id}, label='{self.label}', "
            f"status='{self.status.value}')>"
        )
