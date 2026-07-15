"""SQLAlchemy ORM model definitions.

All models are exported from this package for convenient imports::

    from app.models import Employee, Project, Seat, SeatAllocation
"""

from app.models.employee import Employee
from app.models.project import Project
from app.models.seat import Seat
from app.models.seat_allocation import SeatAllocation

__all__ = [
    "Employee",
    "Project",
    "Seat",
    "SeatAllocation",
]
