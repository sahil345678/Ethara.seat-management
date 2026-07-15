import pytest
from datetime import date
from app.services.employee_service import EmployeeService
from app.schemas.employee import EmployeeCreate
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.project_repo import ProjectRepository
from app.repositories.seat_repo import SeatRepository
from app.repositories.allocation_repo import AllocationRepository
from app.services.dashboard_service import DashboardService
from app.core.enums import EmployeeStatus
from app.core.exceptions import DuplicateEmailError

def test_employee_service_create(db_session):
    """Verify Service Layer handles validation and delegates creation to Repo."""
    svc = EmployeeService(EmployeeRepository(db_session), ProjectRepository(db_session))
    
    schema = EmployeeCreate(
        employee_code="ETH-200",
        name="Service Emp",
        email="service@ethara.com",
        department="QA",
        role="Tester",
        joining_date=date(2025, 1, 1),
        status=EmployeeStatus.ACTIVE
    )
    
    emp = svc.create_employee(schema)
    assert emp.email == "service@ethara.com"
    
    # Verify business rule: Duplicate emails fail at service layer
    with pytest.raises(DuplicateEmailError):
        svc.create_employee(schema)

def test_dashboard_service_summary(db_session):
    """Verify Dashboard aggregation queries execute correctly on the database."""
    emp_repo = EmployeeRepository(db_session)
    seat_repo = SeatRepository(db_session)
    alloc_repo = AllocationRepository(db_session)
    proj_repo = ProjectRepository(db_session)
    
    svc = DashboardService(emp_repo, seat_repo, alloc_repo, proj_repo)
    summary = svc.get_summary()
    
    # Assert properties exist (values will be 0 on pristine db, but shouldn't crash)
    assert hasattr(summary, "total_employees")
    assert hasattr(summary, "total_seats")
    assert hasattr(summary, "occupied_seats")
