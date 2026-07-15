"""Employee repository for database operations."""

import uuid
from typing import Sequence

from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import EmployeeStatus
from app.models.employee import Employee


class EmployeeRepository:
    """Repository for the Employee entity."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, employee_id: uuid.UUID) -> Employee | None:
        """Fetch an employee by UUID, eagerly loading the associated project."""
        stmt = select(Employee).where(Employee.id == employee_id).options(
            joinedload(Employee.project)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_email(self, email: str) -> Employee | None:
        """Fetch an employee by their exact email."""
        stmt = select(Employee).where(Employee.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_employee_code(self, employee_code: str) -> Employee | None:
        """Fetch an employee by their unique code."""
        stmt = select(Employee).where(Employee.employee_code == employee_code)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_employees(
        self,
        status: EmployeeStatus | None = None,
        project_id: uuid.UUID | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "name",
        sort_desc: bool = False,
    ) -> tuple[Sequence[Employee], int]:
        """List employees with filtering, search, sorting, and pagination."""
        stmt = select(Employee)

        if status:
            stmt = stmt.where(Employee.status == status)
        if project_id:
            stmt = stmt.where(Employee.project_id == project_id)
        if search:
            # Leverages the pg_trgm index on `name` for ILIKE, and also
            # searches email and employee_code
            stmt = stmt.where(
                or_(
                    Employee.name.ilike(f"%{search}%"),
                    Employee.email.ilike(f"%{search}%"),
                    Employee.employee_code.ilike(f"%{search}%"),
                )
            )

        # Count total matching records
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar_one()

        # Apply sorting
        sort_col = getattr(Employee, sort_by, Employee.name)
        if sort_desc:
            stmt = stmt.order_by(desc(sort_col))
        else:
            stmt = stmt.order_by(asc(sort_col))

        # Eager load the project to prevent N+1 queries when Pydantic serializes,
        # then apply pagination
        stmt = stmt.options(joinedload(Employee.project)).offset(skip).limit(limit)
        items = self.db.execute(stmt).scalars().all()

        return items, total

    def create(self, employee: Employee) -> Employee:
        """Add a new employee to the database."""
        self.db.add(employee)
        self.db.flush()
        return employee

    def update(self, employee: Employee) -> Employee:
        """Update an existing employee in the database."""
        self.db.add(employee)
        self.db.flush()
        return employee

    def delete(self, employee: Employee) -> None:
        """Delete an employee from the database."""
        self.db.delete(employee)
        self.db.flush()
