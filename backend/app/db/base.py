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


