import pytest
from datetime import date
from app.services.allocation_service import AllocationService
from app.models.employee import Employee
from app.models.seat import Seat
from app.core.enums import EmployeeStatus, SeatStatus, AllocationStatus
from app.core.exceptions import SeatNotAvailableException, ActiveAllocationExistsException

def create_mock_data(db_session):
    """Helper to seed the SQLite DB with required entities for allocation tests."""
    emp = Employee(
        employee_code="ETH-001",
        name="John Engine",
        email="engine@ethara.com",
        department="Engineering",
        role="Developer",
        joining_date=date(2025, 1, 1),
        status=EmployeeStatus.ACTIVE
    )
    
    s1 = Seat(floor=1, zone="A", bay=1, seat_number="1A-01", status=SeatStatus.AVAILABLE)
    s2 = Seat(floor=1, zone="A", bay=1, seat_number="1A-02", status=SeatStatus.RESERVED)
    
    db_session.add_all([emp, s1, s2])
    db_session.commit()
    
    return emp.id, s1.id, s2.id

def test_allocate_seat_manually_success(db_session):
    """Verify manual allocation transitions seat status and returns ACTIVE allocation."""
    emp_id, seat_id, _ = create_mock_data(db_session)
    
    allocation = AllocationService.allocate_seat_manually(db_session, emp_id, seat_id)
    
    assert allocation.status == AllocationStatus.ACTIVE
    assert allocation.employee_id == emp_id
    assert allocation.seat_id == seat_id
    
    seat = db_session.query(Seat).get(seat_id)
    assert seat.status == SeatStatus.OCCUPIED

def test_allocate_seat_manually_reserved_fails(db_session):
    """Verify we cannot assign an employee to a seat locked in RESERVED state."""
    emp_id, _, reserved_seat_id = create_mock_data(db_session)
    
    with pytest.raises(SeatNotAvailableException):
        AllocationService.allocate_seat_manually(db_session, emp_id, reserved_seat_id)

def test_allocate_seat_manually_double_allocation_fails(db_session):
    """Verify business rule: an employee cannot hold two active seats at once."""
    emp_id, seat_id, _ = create_mock_data(db_session)
    
    # First allocation succeeds
    AllocationService.allocate_seat_manually(db_session, emp_id, seat_id)
    
    # Second allocation (even if we had a new seat) must fail
    new_seat = Seat(floor=1, zone="B", bay=1, seat_number="1B-01", status=SeatStatus.AVAILABLE)
    db_session.add(new_seat)
    db_session.commit()
    
    with pytest.raises(ActiveAllocationExistsException):
        AllocationService.allocate_seat_manually(db_session, emp_id, new_seat.id)

def test_release_seat_success(db_session):
    """Verify releasing a seat marks the allocation RELEASED and seat AVAILABLE."""
    emp_id, seat_id, _ = create_mock_data(db_session)
    
    allocation = AllocationService.allocate_seat_manually(db_session, emp_id, seat_id)
    released = AllocationService.release_seat(db_session, allocation.id)
    
    assert released.status == AllocationStatus.RELEASED
    
    seat = db_session.query(Seat).get(seat_id)
    assert seat.status == SeatStatus.AVAILABLE
