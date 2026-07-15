import pytest
from pydantic import ValidationError
from datetime import date
from app.schemas.employee import EmployeeCreate
from app.schemas.project import ProjectCreate

def test_employee_create_valid():
    """Verify that a valid payload instantiates perfectly."""
    emp = EmployeeCreate(
        employee_code="ETH-001",
        name="John Doe",
        email="john.doe@ethara.com",
        department="Engineering",
        role="Developer",
        joining_date=date(2025, 1, 1)
    )
    assert emp.email == "john.doe@ethara.com"
    assert emp.name == "John Doe"

def test_employee_create_invalid_email():
    """Verify that pydantic rejects malformed email strings."""
    with pytest.raises(ValidationError) as exc_info:
        EmployeeCreate(
            employee_code="ETH-002",
            name="Jane Doe",
            email="invalid-email",
            department="Engineering",
            role="Developer",
            joining_date=date(2025, 1, 1)
        )
    assert "value is not a valid email address" in str(exc_info.value)

def test_project_create_valid():
    """Verify Project payload instantiation."""
    proj = ProjectCreate(
        name="Project Alpha",
        description="Top secret",
        manager_name="Alice"
    )
    assert proj.name == "Project Alpha"
