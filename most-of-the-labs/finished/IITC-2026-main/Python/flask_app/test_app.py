"""
Tests for the Flask application.
Run with: pytest test_app.py -v
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test the home page returns 200 OK."""
    response = client.get('/')
    assert response.status_code == 200
    # Check that the response contains expected text
    assert b'Flask' in response.data or b'Hello' in response.data


def test_api_students_list(client):
    """Test GET /api/students returns a list."""
    response = client.get('/api/students')
    assert response.status_code == 200
    data = response.get_json()
    # Should return a list
    assert isinstance(data, list)


def test_api_create_student(client):
    """Test POST /api/students creates a new student."""
    new_student = {
        'name': 'Test Student',
        'email': 'test@example.com'
    }
    response = client.post('/api/students', json=new_student)
    
    # Should return 201 Created
    assert response.status_code == 201
    
    # Check the returned data
    data = response.get_json()
    assert data['name'] == 'Test Student'
    assert data['email'] == 'test@example.com'
    assert 'id' in data  # Should have an ID assigned


def test_api_get_single_user(client):
    """Test GET /users/<id> returns a single user."""
    response = client.get('/users/1')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'id' in data
    assert data['id'] == 1


def test_api_user_not_found(client):
    """Test GET /users/<id> with invalid ID returns 404."""
    response = client.get('/users/9999')
    assert response.status_code == 404


def test_request_inspector(client):
    """Test the /inspect endpoint returns request info."""
    response = client.get('/inspect?test=value')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'method' in data
    assert data['method'] == 'GET'
    assert 'query_args' in data
