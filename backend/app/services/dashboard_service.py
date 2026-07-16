"""Dashboard analytics service."""

import logging
from collections import defaultdict

from app.core.enums import AllocationStatus, EmployeeStatus, SeatStatus
from app.repositories.allocation_repo import AllocationRepository
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.project_repo import ProjectRepository
from app.repositories.seat_repo import SeatRepository
from app.schemas.dashboard import (
    DashboardSummary,
    FloorUtilization,
    ProjectUtilization,
)

logger = logging.getLogger(__name__)


class DashboardService:
    """Service layer for aggregated analytics data.

    Calculates KPI metrics dynamically without bypassing the Repository Layer.
    Uses efficient count queries and in-memory aggregations.
    """

    def __init__(
        self,
        employee_repo: EmployeeRepository,
        seat_repo: SeatRepository,
        allocation_repo: AllocationRepository,
        project_repo: ProjectRepository,
    ) -> None:
        self.employee_repo = employee_repo
        self.seat_repo = seat_repo
        self.allocation_repo = allocation_repo
        self.project_repo = project_repo

    def get_summary(self) -> DashboardSummary:
        """Calculate global KPIs for the dashboard overview."""
        # Using limit=1 to run fast count queries over the subqueries
        _, total_employees = self.employee_repo.list_employees(limit=1)
        _, total_seats = self.seat_repo.list_seats(limit=1, include_occupants=False)
        _, occupied = self.seat_repo.list_seats(
            status=SeatStatus.OCCUPIED, limit=1, include_occupants=False
        )
        _, available = self.seat_repo.list_seats(
            status=SeatStatus.AVAILABLE, limit=1, include_occupants=False
        )
        _, reserved = self.seat_repo.list_seats(
            status=SeatStatus.RESERVED, limit=1, include_occupants=False
        )
        _, maintenance = self.seat_repo.list_seats(
            status=SeatStatus.MAINTENANCE, limit=1, include_occupants=False
        )

        _, active_emps = self.employee_repo.list_employees(
            status=EmployeeStatus.ACTIVE, limit=1
        )
        _, active_allocs = self.allocation_repo.list_allocations(
            status=AllocationStatus.ACTIVE, limit=1
        )

        # Active employees who don't have an active seat allocation
        pending = max(0, active_emps - active_allocs)

        occupancy_rate = (
            (occupied / total_seats * 100) if total_seats > 0 else 0.0
        )

        return DashboardSummary(
            total_employees=total_employees,
            total_seats=total_seats,
            occupied_seats=occupied,
            available_seats=available,
            reserved_seats=reserved,
            maintenance_seats=maintenance,
            occupancy_rate=round(occupancy_rate, 2),
            pending_allocation=pending,
        )

    def get_project_utilization(self) -> list[ProjectUtilization]:
        """Calculate seat utilization broken down by project."""
        projects, _ = self.project_repo.list_projects(limit=1000)

        result = []
        for p in projects:
            _, emp_count = self.employee_repo.list_employees(
                project_id=p.id, limit=1
            )
            _, alloc_count = self.allocation_repo.list_allocations(
                project_id=p.id, status=AllocationStatus.ACTIVE, limit=1
            )
            result.append(
                ProjectUtilization(
                    project_id=p.id,
                    project_name=p.name,
                    allocated_seats=alloc_count,
                    employee_count=emp_count,
                )
            )

        # Sort descending by allocated seats for the chart
        result.sort(key=lambda x: x.allocated_seats, reverse=True)
        return result

    def get_floor_utilization(self) -> list[FloorUtilization]:
        """Calculate seat distribution and statuses broken down by floor."""
        # Load all seats into memory for efficient single-pass aggregation
        seats, _ = self.seat_repo.list_seats(limit=20000, include_occupants=False)

        # Structure: floors_data[floor] = { "total": x, "available": y, ... }
        floors_data = defaultdict(
            lambda: {
                "total": 0,
                "available": 0,
                "occupied": 0,
                "reserved": 0,
                "maintenance": 0,
            }
        )

        for s in seats:
            f_data = floors_data[s.floor]
            f_data["total"] += 1
            if s.status == SeatStatus.AVAILABLE:
                f_data["available"] += 1
            elif s.status == SeatStatus.OCCUPIED:
                f_data["occupied"] += 1
            elif s.status == SeatStatus.RESERVED:
                f_data["reserved"] += 1
            elif s.status == SeatStatus.MAINTENANCE:
                f_data["maintenance"] += 1

        result = []
        for floor, stats in sorted(floors_data.items()):
            result.append(
                FloorUtilization(
                    floor=floor,
                    total_seats=stats["total"],
                    available=stats["available"],
                    occupied=stats["occupied"],
                    reserved=stats["reserved"],
                    maintenance=stats["maintenance"],
                )
            )
        return result
