import pytest

def test_api_health(client):
    """Verify the FastAPI routing engine is operational."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_and_get_project(client):
    """End-to-End API test for Projects."""
    payload = {
        "name": "API E2E Project",
        "description": "Integration Test",
        "manager_name": "QA Leader"
    }
    response = client.post("/api/v1/projects/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == "API E2E Project"
    assert "id" in data
    
    # Read it back via HTTP GET
    get_response = client.get(f"/api/v1/projects/{data['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "API E2E Project"

def test_create_employee_api(client):
    """End-to-End API test for Employees."""
    payload = {
        "employee_code": "API-100",
        "name": "API Worker",
        "email": "worker@api.com",
        "department": "QA",
        "role": "Tester",
        "joining_date": "2025-01-01",
        "status": "ACTIVE"
    }
    response = client.post("/api/v1/employees/", json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == "worker@api.com"
    
    # Duplicate email should return 409 Conflict via HTTP
    duplicate_response = client.post("/api/v1/employees/", json=payload)
    assert duplicate_response.status_code == 409
    assert "already exists" in duplicate_response.json()["detail"]

def test_dashboard_api(client):
    """Verify Dashboard Endpoint returns successful aggregation."""
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    assert "total_employees" in response.json()
