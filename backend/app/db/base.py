"""SQLAlchemy declarative base and model registry.

All ORM models are imported at the bottom of this module so that
Alembic's ``target_metadata = Base.metadata`` can detect every table
when generating automatic migrations.

.. important::

   Model imports **must** appear after the ``Base`` class definition
   to break the circular import cycle (models import ``Base`` from
   this module).
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


# ── Import all models so Alembic can detect them ────────────────────────────
# These imports MUST come after Base is defined to avoid circular imports.

from app.models.employee import Employee  # noqa: E402, F401
from app.models.project import Project  # noqa: E402, F401
from app.models.seat import Seat  # noqa: E402, F401
from app.models.seat_allocation import SeatAllocation  # noqa: E402, F401
