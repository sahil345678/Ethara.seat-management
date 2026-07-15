"""SQLAlchemy database repositories.

All repositories are exported from this package for clean imports
in the service layer::

    from app.repositories import EmployeeRepository, ProjectRepository
"""

from app.repositories.allocation_repo import AllocationRepository
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.project_repo import ProjectRepository
from app.repositories.seat_repo import SeatRepository

__all__ = [
    "AllocationRepository",
    "EmployeeRepository",
    "ProjectRepository",
    "SeatRepository",
]
