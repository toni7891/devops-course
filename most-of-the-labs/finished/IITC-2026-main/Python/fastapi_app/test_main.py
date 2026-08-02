"""
Tests for the FastAPI application.
Run with: pytest test_main.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_read_root():
    """Test GET / returns app info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "FastAPI" in data["message"]


def test_list_students():
    """Test GET /students returns list of students."""
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should have initial seed data
    assert len(data) >= 2


def test_create_student_success():
    """Test POST /students creates a new student with valid data."""
    new_student = {
        "name": "Test Student",
        "email": "test_unique@example.com",  # Unique email to avoid duplicate
        "role": "student"
    }
    response = client.post("/students", json=new_student)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Student"
    assert data["email"] == "test_unique@example.com"
    assert "id" in data
    assert data["is_active"] is True


def test_create_student_validation_error():
    """Test POST /students with invalid data returns 422."""
    invalid_student = {
        "name": "A",  # Too short (min 2 chars)
        "email": "invalid-email",  # Invalid email format
        "role": "invalid_role"  # Not in allowed values
    }
    response = client.post("/students", json=invalid_student)
    
    # Should return 422 Unprocessable Entity (validation error)
    assert response.status_code == 422


def test_get_single_student():
    """Test GET /students/{id} returns a single student."""
    response = client.get("/students/1")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "email" in data


def test_get_student_not_found():
    """Test GET /students/{id} with invalid ID returns 404."""
    response = client.get("/students/9999")
    assert response.status_code == 404


def test_query_parameters():
    """Test GET /students with query parameters."""
    response = client.get("/students?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    # Should respect the limit parameter
    assert len(data) <= 1


def test_async_demo():
    """Test the async demo endpoint (may take 5 seconds)."""
    response = client.get("/async-demo")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "elapsed_seconds" in data


# UNCOMMENT FOR AUTH EXERCISE:
# def test_protected_endpoint_no_auth():
#     """Test /protected without token returns 401."""
#     response = client.get("/protected")
#     assert response.status_code == 401
#
# def test_protected_endpoint_with_auth():
#     """Test /protected with valid token returns 200."""
#     response = client.get(
#         "/protected",
#         headers={"Authorization": "Bearer secret-token"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "message" in data
