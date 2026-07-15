"""Employee business logic service."""

import logging
import uuid
from typing import Sequence

from app.core.enums import EmployeeStatus
from app.core.exceptions import (
    AppException,
    DuplicateEmailError,
    EmployeeNotFoundError,
    ProjectNotFoundError,
)
from app.models.employee import Employee
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.project_repo import ProjectRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

logger = logging.getLogger(__name__)


class EmployeeService:
    """Service layer for Employee operations."""

    def __init__(
        self, repo: EmployeeRepository, project_repo: ProjectRepository
    ) -> None:
        self.repo = repo
        self.project_repo = project_repo

    def get_employee(self, employee_id: uuid.UUID) -> Employee:
        """Fetch an employee by ID or raise an exception."""
        employee = self.repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(employee_id)
        return employee

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
        """Retrieve a paginated list of employees."""
        return self.repo.list_employees(
            status=status,
            project_id=project_id,
            search=search,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc,
        )

    def create_employee(self, data: EmployeeCreate) -> Employee:
        """Validate uniqueness and project existence, then create employee."""
        logger.info("Creating employee with email: %s", data.email)

        if self.repo.get_by_email(data.email):
            raise DuplicateEmailError(data.email)

        if self.repo.get_by_employee_code(data.employee_code):
            raise AppException(
                message=f"Employee code '{data.employee_code}' already exists.",
                status_code=409,
            )

        if data.project_id:
            if not self.project_repo.get_by_id(data.project_id):
                raise ProjectNotFoundError(data.project_id)

        employee = Employee(
            employee_code=data.employee_code,
            name=data.name,
            email=data.email,
            department=data.department,
            role=data.role,
            joining_date=data.joining_date,
            status=data.status,
            project_id=data.project_id,
        )
        return self.repo.create(employee)

    def update_employee(
        self, employee_id: uuid.UUID, data: EmployeeUpdate
    ) -> Employee:
        """Validate uniqueness on change, then update employee fields."""
        employee = self.get_employee(employee_id)

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return employee

        # If email is being changed, ensure it's not taken
        if "email" in update_data and update_data["email"] != employee.email:
            if self.repo.get_by_email(update_data["email"]):
                raise DuplicateEmailError(update_data["email"])

        # If project is being reassigned, ensure new project exists
        if "project_id" in update_data and update_data["project_id"]:
            if not self.project_repo.get_by_id(update_data["project_id"]):
                raise ProjectNotFoundError(update_data["project_id"])

        for key, value in update_data.items():
            setattr(employee, key, value)

        logger.info("Updated employee: %s", employee_id)
        return self.repo.update(employee)
