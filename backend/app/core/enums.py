"""Application-wide enumerations.

Every enum inherits from `str` so that values serialize cleanly
to JSON in Pydantic schemas and API responses.
"""

import enum


class EmployeeStatus(str, enum.Enum):
    """Employee employment status."""

    ACTIVE = "Active"
    INACTIVE = "Inactive"


class SeatStatus(str, enum.Enum):
    """Physical seat availability status."""

    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    RESERVED = "Reserved"
    MAINTENANCE = "Maintenance"


class AllocationStatus(str, enum.Enum):
    """Seat allocation lifecycle status."""

    ACTIVE = "Active"
    RELEASED = "Released"


class ProjectStatus(str, enum.Enum):
    """Project lifecycle status."""

    ACTIVE = "Active"
    COMPLETED = "Completed"
