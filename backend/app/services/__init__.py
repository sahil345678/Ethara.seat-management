"""Business logic services.

All services are exported from this package for clean imports
in the API layer::

    from app.services import EmployeeService, ProjectService
"""

from app.services.ai_service import AiService
from app.services.allocation_service import AllocationService
from app.services.dashboard_service import DashboardService
from app.services.employee_service import EmployeeService
from app.services.project_service import ProjectService
from app.services.seat_service import SeatService

__all__ = [
    "AiService",
    "AllocationService",
    "DashboardService",
    "EmployeeService",
    "ProjectService",
    "SeatService",
]
