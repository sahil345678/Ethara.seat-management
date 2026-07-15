"""Initial database schema.

Creates all tables, PostgreSQL enum types, indexes, constraints,
and the pg_trgm extension for the Ethara Seat Allocation system.

Tables created:
    - projects
    - employees (FK → projects)
    - seats
    - seat_allocations (FK → employees, seats, projects)

Revision ID: 0001
Revises: -
Create Date: 2026-07-15
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# ── Revision identifiers ────────────────────────────────────────────────────
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ── PostgreSQL enum type definitions ────────────────────────────────────────
# Defined at module level so they can be reused in both upgrade and downgrade.

project_status_enum = sa.Enum(
    "Active", "Completed",
    name="project_status",
)
employee_status_enum = sa.Enum(
    "Active", "Inactive",
    name="employee_status",
)
seat_status_enum = sa.Enum(
    "Available", "Occupied", "Reserved", "Maintenance",
    name="seat_status",
)
allocation_status_enum = sa.Enum(
    "Active", "Released",
    name="allocation_status",
)


def upgrade() -> None:
    """Apply migration — create extensions, enums, tables, and indexes."""

    # ── 1. PostgreSQL Extensions ─────────────────────────────────────────
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    # ── 2. Enum Types ────────────────────────────────────────────────────
    project_status_enum.create(op.get_bind(), checkfirst=True)
    employee_status_enum.create(op.get_bind(), checkfirst=True)
    seat_status_enum.create(op.get_bind(), checkfirst=True)
    allocation_status_enum.create(op.get_bind(), checkfirst=True)

    # ── 3. Tables ────────────────────────────────────────────────────────

    # ── projects (no dependencies) ───────────────────────────────────────
    op.create_table(
        "projects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("manager_name", sa.String(150), nullable=True),
        sa.Column(
            "status",
            sa.Enum("Active", "Completed", name="project_status", create_type=False),
            nullable=False,
            server_default="Active",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_projects"),
    )

    # ── seats (no dependencies) ──────────────────────────────────────────
    op.create_table(
        "seats",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("floor", sa.Integer(), nullable=False),
        sa.Column("zone", sa.String(10), nullable=False),
        sa.Column("bay", sa.String(10), nullable=False),
        sa.Column("seat_number", sa.String(20), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "Available", "Occupied", "Reserved", "Maintenance",
                name="seat_status",
                create_type=False,
            ),
            nullable=False,
            server_default="Available",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_seats"),
        sa.UniqueConstraint(
            "floor", "zone", "bay", "seat_number",
            name="uq_seat_location",
        ),
    )

    # ── employees (FK → projects) ────────────────────────────────────────
    op.create_table(
        "employees",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("employee_code", sa.String(20), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("department", sa.String(100), nullable=True),
        sa.Column("role", sa.String(100), nullable=True),
        sa.Column("joining_date", sa.Date(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("Active", "Inactive", name="employee_status", create_type=False),
            nullable=False,
            server_default="Active",
        ),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_employees"),
        sa.UniqueConstraint("employee_code", name="uq_employee_code"),
        sa.UniqueConstraint("email", name="uq_employee_email"),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"],
            name="fk_employee_project",
        ),
    )

    # ── seat_allocations (FK → employees, seats, projects) ───────────────
    op.create_table(
        "seat_allocations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("employee_id", sa.Uuid(), nullable=False),
        sa.Column("seat_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column(
            "allocation_status",
            sa.Enum("Active", "Released", name="allocation_status", create_type=False),
            nullable=False,
            server_default="Active",
        ),
        sa.Column(
            "allocation_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "released_date",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_seat_allocations"),
        sa.ForeignKeyConstraint(
            ["employee_id"], ["employees.id"],
            name="fk_allocation_employee",
        ),
        sa.ForeignKeyConstraint(
            ["seat_id"], ["seats.id"],
            name="fk_allocation_seat",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"],
            name="fk_allocation_project",
        ),
    )

    # ── 4. Indexes ───────────────────────────────────────────────────────

    # ── Employee indexes ─────────────────────────────────────────────────
    op.create_index(
        "idx_employee_project", "employees", ["project_id"],
    )
    op.create_index(
        "idx_employee_status", "employees", ["status"],
    )
    op.create_index(
        "idx_employee_name_trgm",
        "employees",
        ["name"],
        postgresql_using="gin",
        postgresql_ops={"name": "gin_trgm_ops"},
    )

    # ── Seat indexes ─────────────────────────────────────────────────────
    op.create_index(
        "idx_seat_status", "seats", ["status"],
    )
    op.create_index(
        "idx_seat_floor_zone", "seats", ["floor", "zone"],
    )

    # ── SeatAllocation indexes ───────────────────────────────────────────
    # Partial unique indexes — enforce business rules at the DB level:
    #   • One employee can have only one active seat.
    #   • One seat can be allocated to only one active employee.
    op.create_index(
        "idx_unique_active_employee",
        "seat_allocations",
        ["employee_id"],
        unique=True,
        postgresql_where=sa.text("allocation_status = 'Active'"),
    )
    op.create_index(
        "idx_unique_active_seat",
        "seat_allocations",
        ["seat_id"],
        unique=True,
        postgresql_where=sa.text("allocation_status = 'Active'"),
    )

    # General-purpose query indexes
    op.create_index(
        "idx_alloc_employee", "seat_allocations", ["employee_id"],
    )
    op.create_index(
        "idx_alloc_seat", "seat_allocations", ["seat_id"],
    )
    op.create_index(
        "idx_alloc_project", "seat_allocations", ["project_id"],
    )
    op.create_index(
        "idx_alloc_status", "seat_allocations", ["allocation_status"],
    )


def downgrade() -> None:
    """Revert migration — drop all tables, enum types, and extensions."""

    # ── 1. Drop indexes (explicit, for clarity — tables drop theirs too) ─
    op.drop_index("idx_alloc_status", table_name="seat_allocations")
    op.drop_index("idx_alloc_project", table_name="seat_allocations")
    op.drop_index("idx_alloc_seat", table_name="seat_allocations")
    op.drop_index("idx_alloc_employee", table_name="seat_allocations")
    op.drop_index("idx_unique_active_seat", table_name="seat_allocations")
    op.drop_index("idx_unique_active_employee", table_name="seat_allocations")
    op.drop_index("idx_seat_floor_zone", table_name="seats")
    op.drop_index("idx_seat_status", table_name="seats")
    op.drop_index("idx_employee_name_trgm", table_name="employees")
    op.drop_index("idx_employee_status", table_name="employees")
    op.drop_index("idx_employee_project", table_name="employees")

    # ── 2. Drop tables (reverse dependency order) ────────────────────────
    op.drop_table("seat_allocations")
    op.drop_table("employees")
    op.drop_table("seats")
    op.drop_table("projects")

    # ── 3. Drop enum types ───────────────────────────────────────────────
    allocation_status_enum.drop(op.get_bind(), checkfirst=True)
    seat_status_enum.drop(op.get_bind(), checkfirst=True)
    employee_status_enum.drop(op.get_bind(), checkfirst=True)
    project_status_enum.drop(op.get_bind(), checkfirst=True)

    # ── 4. Drop extensions ───────────────────────────────────────────────
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
