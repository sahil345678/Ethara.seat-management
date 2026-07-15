"""Project business logic service."""

import logging
import uuid
from typing import Sequence

from app.core.enums import ProjectStatus
from app.core.exceptions import ProjectNotFoundError
from app.models.project import Project
from app.repositories.project_repo import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate

logger = logging.getLogger(__name__)


class ProjectService:
    """Service layer for Project operations.

    Encapsulates business rules and orchestrates repository calls.
    """

    def __init__(self, repo: ProjectRepository) -> None:
        self.repo = repo

    def get_project(self, project_id: uuid.UUID) -> Project:
        """Fetch a project by ID or raise an exception if not found."""
        project = self.repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(project_id)
        return project

    def list_projects(
        self,
        status: ProjectStatus | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "name",
        sort_desc: bool = False,
    ) -> tuple[Sequence[Project], int]:
        """Retrieve a paginated list of projects matching the criteria."""
        return self.repo.list_projects(
            status=status,
            search=search,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc,
        )

    def create_project(self, data: ProjectCreate) -> Project:
        """Create a new project from schema data."""
        logger.info("Creating project: %s", data.name)
        project = Project(
            name=data.name,
            description=data.description,
            manager_name=data.manager_name,
            status=data.status,
        )
        return self.repo.create(project)

    def update_project(
        self, project_id: uuid.UUID, data: ProjectUpdate
    ) -> Project:
        """Update an existing project applying only provided fields."""
        project = self.get_project(project_id)

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return project

        for key, value in update_data.items():
            setattr(project, key, value)

        logger.info("Updated project: %s", project_id)
        return self.repo.update(project)
