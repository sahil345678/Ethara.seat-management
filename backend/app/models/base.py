"""Shared model mixins for timestamp columns.

Provides reusable mixins so that common timestamp columns are
defined once and consistently applied across all ORM models.

Usage:
    - Projects and Seats use ``CreatedAtMixin`` (created_at only).
    - Employees use ``TimestampMixin`` (created_at + updated_at).
"""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    """Adds a server-defaulted ``created_at`` column."""

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    )


class TimestampMixin(CreatedAtMixin):
    """Adds ``created_at`` and ``updated_at`` columns.

    ``updated_at`` is automatically refreshed on every row update
    via SQLAlchemy's ``onupdate`` hook.
    """

    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )
