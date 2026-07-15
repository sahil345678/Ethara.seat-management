"""Database seeding system for Phase 9.

Generates realistic test data for the Ethara Seat Allocation System using Faker.
Adheres strictly to the architectural requirements and constraints.

Usage:
    export PYTHONPATH=.
    python app/db/seed.py
"""

import logging
import random
import uuid
from datetime import datetime, timedelta, timezone

from faker import Faker

from app.core.enums import AllocationStatus, EmployeeStatus, ProjectStatus, SeatStatus
from app.db.session import SessionLocal
from app.models.employee import Employee
from app.models.project import Project
from app.models.seat import Seat
from app.models.seat_allocation import SeatAllocation

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

fake = Faker()
Faker.seed(42)  # For reproducible random names/departments
random.seed(42)

def seed_db() -> None:
    """Populate the database with realistic data in batches."""
    db = SessionLocal()
    try:
        # Check for idempotency
        if db.query(Project).count() > 0:
            logger.info("Database already contains projects. Seeding skipped.")
            return

        logger.info("Starting database seed process...")

        # 1. Projects (11)
        project_names = [
            "Project Indigo", "Project Talos", "Project Helios", "Ethara Core",
            "Project Nexus", "Apollo Initiative", "Project Athena", "Titan Framework",
            "Project Orion", "Aurora System", "Vanguard Platform"
        ]
        projects = []
        for name in project_names:
            projects.append(Project(
                id=uuid.uuid4(),
                name=name,
                description=fake.catch_phrase(),
                manager_name=fake.name(),
                status=ProjectStatus.ACTIVE
            ))
        db.add_all(projects)
        db.commit()
        logger.info(f"Seeded {len(projects)} projects.")

        # 2. Seats (5,500 total)
        # 5 Floors * 10 Zones (A-J) * 11 Bays * 10 Seats = 5,500 seats
        seats = []
        zones = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for floor in range(1, 6):
            for zone in zones:
                for bay in range(1, 12):
                    for seat_num in range(1, 11):
                        seats.append(Seat(
                            id=uuid.uuid4(),
                            floor=floor,
                            zone=zone,
                            bay=str(bay),
                            seat_number=f"{zone}{bay}-{seat_num:02d}",
                            status=SeatStatus.AVAILABLE
                        ))
        
        # Shuffle seats to distribute statuses randomly across the building
        random.shuffle(seats)
        
        # Distribute statuses based on requirements
        # Total: 5,500. Occupied: 4,950, Reserved: 100, Available: 450
        occupied_seats = seats[:4950]
        reserved_seats = seats[4950:5050]
        available_seats = seats[5050:]
        
        for s in occupied_seats:
            s.status = SeatStatus.OCCUPIED
        for s in reserved_seats:
            s.status = SeatStatus.RESERVED
        for s in available_seats:
            s.status = SeatStatus.AVAILABLE
            
        chunk_size = 1000
        for i in range(0, len(seats), chunk_size):
            db.add_all(seats[i:i + chunk_size])
            db.commit()
        logger.info(f"Seeded {len(seats)} seats (4950 Occupied, 100 Reserved, 450 Available).")

        # 3. Employees (5,000 total)
        employees = []
        departments = ["Engineering", "Product", "HR", "Finance", "Design", "Marketing", "Sales", "Support"]
        roles = ["Software Engineer", "Product Manager", "Product Designer", "QA Engineer", "Data Scientist", "Analyst", "Team Lead"]
        
        for i in range(5000):
            emp_id = uuid.uuid4()
            # Enforce unique emails and employee codes
            emp_code = f"ETH-{i+1:05d}"
            email = f"eth{i+1:05d}@{fake.free_email_domain()}"
            
            employees.append(Employee(
                id=emp_id,
                employee_code=emp_code,
                name=fake.name(),
                email=email,
                department=random.choice(departments),
                role=random.choice(roles),
                joining_date=fake.date_between(start_date='-5y', end_date='today'),
                status=EmployeeStatus.ACTIVE,
                project_id=random.choice(projects).id
            ))
            
        random.shuffle(employees)
        
        # 4,950 employees get allocated. 50 are left pending without a seat.
        allocated_emps = employees[:4950]
        pending_emps = employees[4950:]
        
        for i in range(0, len(employees), chunk_size):
            db.add_all(employees[i:i + chunk_size])
            db.commit()
        logger.info(f"Seeded {len(employees)} employees (4950 allocated, 50 pending).")

        # 4. Seat Allocations (4,950 total)
        allocations = []
        for i, emp in enumerate(allocated_emps):
            seat = occupied_seats[i]
            allocations.append(SeatAllocation(
                id=uuid.uuid4(),
                employee_id=emp.id,
                seat_id=seat.id,
                project_id=emp.project_id,
                allocation_status=AllocationStatus.ACTIVE,
                allocation_date=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 365))
            ))
            
        for i in range(0, len(allocations), chunk_size):
            db.add_all(allocations[i:i + chunk_size])
            db.commit()
            
        logger.info(f"Seeded {len(allocations)} active seat allocations.")
        logger.info("Database seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
