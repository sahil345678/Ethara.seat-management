"""Project repository for database operations."""

import uuid
from typing import Sequence

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.core.enums import ProjectStatus
from app.models.project import Project


class ProjectRepository:
    """Repository for the Project entity.

    Handles all CRUD, search, filtering, and pagination.
    Does not contain business logic.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, project_id: uuid.UUID) -> Project | None:
        """Fetch a project by UUID."""
        stmt = select(Project).where(Project.id == project_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_name(self, name: str) -> Project | None:
        """Fetch a project by its exact name."""
        stmt = select(Project).where(Project.name == name)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_projects(
        self,
        status: ProjectStatus | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "name",
        sort_desc: bool = False,
    ) -> tuple[Sequence[Project], int]:
        """List projects with filtering, search, sorting, and pagination."""
        stmt = select(Project)

        if status:
            stmt = stmt.where(Project.status == status)
        if search:
            stmt = stmt.where(Project.name.ilike(f"%{search}%"))

        # Count total matching records before applying pagination
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar_one()

        # Apply sorting
        sort_col = getattr(Project, sort_by, Project.name)
        if sort_desc:
            stmt = stmt.order_by(desc(sort_col))
        else:
            stmt = stmt.order_by(asc(sort_col))

        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        items = self.db.execute(stmt).scalars().all()

        return items, total

    def create(self, project: Project) -> Project:
        """Add a new project to the database."""
        self.db.add(project)
        self.db.flush()
        return project

    def update(self, project: Project) -> Project:
        """Update an existing project in the database."""
        self.db.add(project)
        self.db.flush()
        return project

    def delete(self, project: Project) -> None:
        """Delete a project from the database."""
        self.db.delete(project)
        self.db.flush()
