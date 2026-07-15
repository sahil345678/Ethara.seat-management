"""Seat Allocation Engine business logic service."""

import logging
import uuid
from collections import Counter
from datetime import datetime, timezone
from typing import Sequence

from app.core.enums import AllocationStatus, EmployeeStatus, SeatStatus
from app.core.exceptions import (
    AppException,
    EmployeeAlreadyAllocatedError,
    EmployeeNotFoundError,
    InactiveEmployeeError,
    NoAvailableSeatsError,
    SeatMaintenanceError,
    SeatNotFoundError,
    SeatOccupiedError,
    SeatReservedError,
)
from app.models.employee import Employee
from app.models.seat import Seat
from app.models.seat_allocation import SeatAllocation
from app.repositories.allocation_repo import AllocationRepository
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.seat_repo import SeatRepository
from app.schemas.seat_allocation import SeatAllocateRequest

logger = logging.getLogger(__name__)


class AllocationService:
    """Core Seat Allocation Engine.

    Manages complex seat allocation logic, race-condition protection via
    row-level locking, and the auto-allocation proximity algorithm.
    """

    def __init__(
        self,
        repo: AllocationRepository,
        seat_repo: SeatRepository,
        employee_repo: EmployeeRepository,
    ) -> None:
        self.repo = repo
        self.seat_repo = seat_repo
        self.employee_repo = employee_repo

    def get_allocation(self, allocation_id: uuid.UUID) -> SeatAllocation:
        """Fetch an allocation by ID or raise an exception."""
        allocation = self.repo.get_by_id(allocation_id)
        if not allocation:
            raise AppException("Seat allocation not found.", status_code=404)
        return allocation

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
        """Retrieve a paginated list of seat allocations."""
        return self.repo.list_allocations(
            employee_id=employee_id,
            seat_id=seat_id,
            project_id=project_id,
            status=status,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc,
        )

    def allocate_seat(self, data: SeatAllocateRequest) -> SeatAllocation:
        """Allocate a seat to an employee (Manual or Auto)."""
        logger.info("Starting allocation process for employee %s", data.employee_id)

        # 1. Validate Employee Rules
        employee = self.employee_repo.get_by_id(data.employee_id)
        if not employee:
            raise EmployeeNotFoundError(data.employee_id)
        if employee.status != EmployeeStatus.ACTIVE:
            raise InactiveEmployeeError(data.employee_id)

        existing_alloc = self.repo.get_active_for_employee(data.employee_id)
        if existing_alloc:
            raise EmployeeAlreadyAllocatedError(data.employee_id)

        # 2. Branch to Manual vs Auto
        if data.seat_id:
            return self._allocate_manual(employee, data.seat_id)
        else:
            return self._allocate_auto(employee)

    def _allocate_manual(
        self, employee: Employee, seat_id: uuid.UUID
    ) -> SeatAllocation:
        """Manually allocate a specific seat using row locking."""
        seat = self.seat_repo.get_by_id(seat_id)
        if not seat:
            raise SeatNotFoundError(seat_id)

        try:
            # Row-level lock via ORM refresh (`SELECT ... FOR UPDATE`)
            self.seat_repo.db.refresh(seat, with_for_update=True)

            # Re-verify seat status while locked
            if seat.status == SeatStatus.OCCUPIED:
                raise SeatOccupiedError(seat_id)
            if seat.status == SeatStatus.RESERVED:
                raise SeatReservedError(seat_id)
            if seat.status == SeatStatus.MAINTENANCE:
                raise SeatMaintenanceError(seat_id)
            if seat.status != SeatStatus.AVAILABLE:
                raise AppException("Seat is not available.", status_code=400)

            # Create the allocation record
            allocation = SeatAllocation(
                employee_id=employee.id,
                seat_id=seat.id,
                project_id=employee.project_id,
                allocation_status=AllocationStatus.ACTIVE,
                allocation_date=datetime.now(timezone.utc),
            )
            seat.status = SeatStatus.OCCUPIED

            created_alloc = self.repo.create(allocation)
            self.seat_repo.update(seat)

            self.repo.db.commit()
            logger.info("Manually allocated seat %s to employee %s", seat.id, employee.id)
            return self.repo.get_by_id(created_alloc.id)

        except (SeatOccupiedError, SeatReservedError, SeatMaintenanceError, AppException):
            self.repo.db.rollback()
            raise
        except Exception as e:
            self.repo.db.rollback()
            logger.error("Database transaction failed during manual allocation: %s", e)
            raise AppException("Internal server error during allocation.", status_code=500)

    def _allocate_auto(self, employee: Employee) -> SeatAllocation:
        """Automatically allocate the best available seat using the proximity algorithm."""
        best_seats = self._rank_available_seats(employee.project_id)
        if not best_seats:
            raise NoAvailableSeatsError()

        # Iterate through ranked seats to handle potential race conditions
        for seat in best_seats:
            try:
                # Attempt to lock the row
                self.seat_repo.db.refresh(seat, with_for_update=True)

                if seat.status != SeatStatus.AVAILABLE:
                    self.seat_repo.db.rollback()
                    continue  # Another transaction took it; try the next best seat

                # Successfully locked and verified
                allocation = SeatAllocation(
                    employee_id=employee.id,
                    seat_id=seat.id,
                    project_id=employee.project_id,
                    allocation_status=AllocationStatus.ACTIVE,
                    allocation_date=datetime.now(timezone.utc),
                )
                seat.status = SeatStatus.OCCUPIED

                created_alloc = self.repo.create(allocation)
                self.seat_repo.update(seat)
                self.repo.db.commit()

                logger.info("Auto-allocated seat %s to employee %s", seat.id, employee.id)
                return self.repo.get_by_id(created_alloc.id)

            except Exception as e:
                self.repo.db.rollback()
                logger.warning("Race condition locking seat %s, trying next. Error: %s", seat.id, e)
                continue

        raise NoAvailableSeatsError(
            "Could not secure an available seat due to concurrent allocations. Please try again."
        )

    def _rank_available_seats(self, project_id: uuid.UUID | None) -> list[Seat]:
        """Rank available seats based on project team proximity."""
        available_seats, _ = self.seat_repo.list_seats(
            status=SeatStatus.AVAILABLE, limit=5000
        )
        if not available_seats or not project_id:
            return list(available_seats)

        # Locate teammates in the same project
        teammate_allocs, _ = self.repo.list_allocations(
            project_id=project_id, status=AllocationStatus.ACTIVE, limit=5000
        )
        teammate_seats = [a.seat for a in teammate_allocs if a.seat]

        if not teammate_seats:
            return list(available_seats)

        # Determine the "center of gravity" for the project
        floor_counts = Counter(s.floor for s in teammate_seats)
        zone_counts = Counter((s.floor, s.zone) for s in teammate_seats)
        bay_counts = Counter((s.floor, s.zone, s.bay) for s in teammate_seats)

        target_floor = floor_counts.most_common(1)[0][0]
        target_zone = zone_counts.most_common(1)[0][0][1]
        target_bay = bay_counts.most_common(1)[0][0][2]

        def score_seat(s: Seat) -> int:
            """Score seats strictly following business rules."""
            if s.floor == target_floor:
                if s.zone == target_zone:
                    if s.bay == target_bay:
                        return 3  # Same floor, zone, bay
                    return 2  # Same floor, zone, alternate bay
                return 1  # Same floor, alternate zone
            return 0  # Alternate floor

        # Sort descending by score, ensuring proximity rules are met
        return sorted(available_seats, key=score_seat, reverse=True)

    def release_seat(
        self, employee_id: uuid.UUID | None = None, seat_id: uuid.UUID | None = None
    ) -> SeatAllocation:
        """Release an active seat allocation, making the seat available again."""
        allocation = None
        if employee_id:
            allocation = self.repo.get_active_for_employee(employee_id)
        elif seat_id:
            allocation = self.repo.get_active_for_seat(seat_id)

        if not allocation:
            raise AppException("No active allocation found to release.", status_code=404)

        try:
            seat = allocation.seat
            # Lock the seat before releasing
            self.seat_repo.db.refresh(seat, with_for_update=True)

            allocation.allocation_status = AllocationStatus.RELEASED
            allocation.released_date = datetime.now(timezone.utc)
            seat.status = SeatStatus.AVAILABLE

            self.repo.update(allocation)
            self.seat_repo.update(seat)

            self.repo.db.commit()
            logger.info("Released allocation %s", allocation.id)
            return allocation

        except Exception as e:
            self.repo.db.rollback()
            logger.error("Failed to release seat allocation: %s", e)
            raise AppException("Internal server error while releasing seat.", status_code=500)
