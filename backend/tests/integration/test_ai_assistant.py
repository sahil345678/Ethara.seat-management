import pytest
from app.services.ai_service import AiService
from app.services.employee_service import EmployeeService
from app.services.project_service import ProjectService
from app.services.seat_service import SeatService
from app.services.dashboard_service import DashboardService
from app.services.allocation_service import AllocationService
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.project_repo import ProjectRepository
from app.repositories.seat_repo import SeatRepository
from app.repositories.allocation_repo import AllocationRepository

def test_ai_fallback_regex_routing(db_session):
    """Verify the AI service gracefully falls back to Regex and executes internal service calls if Gemini is unavailable."""
    emp_repo = EmployeeRepository(db_session)
    proj_repo = ProjectRepository(db_session)
    seat_repo = SeatRepository(db_session)
    alloc_repo = AllocationRepository(db_session)
    
    ai_service = AiService(
        employee_service=EmployeeService(emp_repo, proj_repo),
        project_service=ProjectService(proj_repo),
        seat_service=SeatService(seat_repo),
        dashboard_service=DashboardService(emp_repo, seat_repo, alloc_repo, proj_repo),
        allocation_service=AllocationService(alloc_repo, emp_repo, seat_repo)
    )
    
    # Force fallback by overriding the Gemini model
    ai_service.model = None
    
    # Test Intent: LOCATE_EMPLOYEE (Regex: "where is ... seated")
    response = ai_service.process_query("where is my seat")
    assert "Please specify the full name of the employee." in response or "I couldn't find any employee" in response
    
    # Test Intent: PENDING_ALLOCATIONS (Regex: "pending")
    response = ai_service.process_query("pending seat allocations")
    assert "There are currently 0 employees pending seat allocation" in response
    
    # Test Intent: Unknown Request
    response = ai_service.process_query("what is the weather like today")
    assert "I couldn't understand your request." in response
