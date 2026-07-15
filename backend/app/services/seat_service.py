"""Seat business logic service."""

import logging
import uuid
from typing import Sequence

from app.core.enums import SeatStatus
from app.core.exceptions import DuplicateSeatError, SeatNotFoundError
from app.models.seat import Seat
from app.repositories.seat_repo import SeatRepository
from app.schemas.seat import SeatCreate, SeatUpdate

logger = logging.getLogger(__name__)


class SeatService:
    """Service layer for Seat operations."""

    def __init__(self, repo: SeatRepository) -> None:
        self.repo = repo

    def get_seat(self, seat_id: uuid.UUID) -> Seat:
        """Fetch a seat by ID or raise an exception."""
        seat = self.repo.get_by_id(seat_id)
        if not seat:
            raise SeatNotFoundError(seat_id)
        return seat

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
        """Retrieve a paginated list of seats."""
        return self.repo.list_seats(
            floor=floor,
            zone=zone,
            status=status,
            search=search,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc,
        )

    def create_seat(self, data: SeatCreate) -> Seat:
        """Validate location uniqueness and create seat."""
        label = f"F{data.floor}-Z{data.zone}-B{data.bay}-{data.seat_number}"
        logger.info("Creating seat: %s", label)

        if self.repo.get_by_location(
            data.floor, data.zone, data.bay, data.seat_number
        ):
            raise DuplicateSeatError(label)

        seat = Seat(
            floor=data.floor,
            zone=data.zone,
            bay=data.bay,
            seat_number=data.seat_number,
            status=data.status,
        )
        return self.repo.create(seat)

    def update_seat(self, seat_id: uuid.UUID, data: SeatUpdate) -> Seat:
        """Validate location uniqueness if modified, then update seat."""
        seat = self.get_seat(seat_id)

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return seat

        new_floor = update_data.get("floor", seat.floor)
        new_zone = update_data.get("zone", seat.zone)
        new_bay = update_data.get("bay", seat.bay)
        new_num = update_data.get("seat_number", seat.seat_number)

        # If any part of the physical location changed, ensure the new slot is free
        if (
            new_floor != seat.floor
            or new_zone != seat.zone
            or new_bay != seat.bay
            or new_num != seat.seat_number
        ):
            if self.repo.get_by_location(new_floor, new_zone, new_bay, new_num):
                new_label = f"F{new_floor}-Z{new_zone}-B{new_bay}-{new_num}"
                raise DuplicateSeatError(new_label)

        for key, value in update_data.items():
            setattr(seat, key, value)

        logger.info("Updated seat: %s", seat_id)
        return self.repo.update(seat)
