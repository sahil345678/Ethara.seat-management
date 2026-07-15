import os
import sys

# Set environment variables for testing before loading application code
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["GEMINI_API_KEY"] = "mock_api_key_for_testing"
os.environ["POSTGRES_USER"] = "postgres"
os.environ["POSTGRES_PASSWORD"] = "postgres"
os.environ["POSTGRES_DB"] = "test_ethara"

# Ensure the backend root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.base import Base
from app.api.deps import get_db
from app.main import app

# Use an on-disk SQLite database for isolated transactional testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    """Create the test database tables once per test session."""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    # Cleanup sqlite file
    if os.path.exists("./test.db"):
        try:
            os.remove("./test.db")
        except OSError:
            pass

@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Provide a transactional scope around each test.
    Rollback at the end of the test to keep the database perfectly pristine.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Provide a FastAPI TestClient configured to use the transactional test database session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
