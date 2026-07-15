import pytest
from datetime import date
from app.models.employee import Employee
from app.core.enums import EmployeeStatus
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.project_repo import ProjectRepository

def test_employee_repo_create_and_read(db_session):
    """Validate Repository CRUD layer against an actual SQLite session."""
    repo = EmployeeRepository(db_session)
    
    # Verify Create
    emp = Employee(
        employee_code="ETH-100",
        name="Repo Test Emp",
        email="repo@ethara.com",
        department="QA",
        joining_date=date(2025, 1, 1),
        status=EmployeeStatus.ACTIVE
    )
    created = repo.create(emp)
    assert created.id is not None
    
    # Verify Read
    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.name == "Repo Test Emp"
    
    # Verify List (Pagination)
    results, total = repo.list_employees(skip=0, limit=10)
    assert total >= 1
    assert len(results) >= 1
    
    # Verify Email Unique Lookup
    by_email = repo.get_by_email("repo@ethara.com")
    assert by_email is not None
    assert by_email.id == created.id
