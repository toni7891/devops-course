# Python Testing Lab — From Zero to Test Hero

> **Why test?** Tests catch bugs before users do, document how code works, and let you refactor with confidence.

---

## Chapter 1: Testing Basics with pytest

### What is pytest?

**pytest** = The most popular Python testing framework. It finds and runs your tests automatically.

### Setup

```bash
# Install pytest
pip install pytest

# Verify installation
pytest --version
```

### Your First Test — Fix the Broken Tests!

A file `test_example.py` is already created for you. It has broken tests that need fixing.

```bash
# Run the tests (they will fail - that's the exercise!)
pytest test_example.py -v
```

**Expected Output (before fixing):**
```
test_example.py::test_add FAILED
test_example.py::test_subtract FAILED
test_example.py::test_multiply FAILED
```

**Your Task:**
1. Open `test_example.py`
2. Look at the `FIXME` comments
3. Fix the assert statements so tests pass
4. Run again until all tests pass!

**Example fix:**
```python
# Before (broken):
assert result == 6  # FIXME: Change 6 to the correct answer

# After (fixed):
assert result == 5  # Because add(2, 3) returns 5
```

### The `assert` Statement

**What it does:** Checks if something is True

```python
assert 2 + 2 == 4        # ✓ Passes
assert "hello" in "hello world"  # ✓ Passes
assert len([1, 2, 3]) == 3       # ✓ Passes

assert 2 + 2 == 5        # ✗ Fails with AssertionError
```

**pytest magic:** When a test fails, pytest shows you exactly what went wrong:
```
AssertionError: assert 4 == 5
```

---

## Chapter 2: Testing Flask Applications

### The Challenge

Flask apps need a test client that simulates HTTP requests without starting a real server.

### Setup

In your `flask_app/` directory:

```bash
pip install pytest
```

### Run the Existing Flask Tests

A test file `test_app.py` already exists in `flask_app/`. Let's run it:

```bash
cd flask_app
pytest test_app.py -v
```

### How Flask Tests Work

Open `test_app.py` to see how it works:

```python
import pytest
from app import app  # Import your Flask app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page returns 200 OK"""
    response = client.get('/')
    assert response.status_code == 200
```

**Key points:**
- `@pytest.fixture` creates a test client
- `client.get('/')` simulates HTTP requests
- No real server needed!

### Understanding the Fixture

**What's a fixture?** 
- A setup function that runs before each test
- `@pytest.fixture` marks it
- Tests that need it add the fixture name as a parameter

**The flow:**
```
pytest finds test_home_page(client)
           ↓
   Sees it needs 'client' fixture
           ↓
   Runs client() fixture → creates test client
           ↓
   Passes client to test_home_page(client)
           ↓
   Test runs
           ↓
   Fixture cleans up (after 'yield')
```

---

## Chapter 5: Mocking — Faking External Services

### Why Mock?

**Problem:** Your code calls external APIs, databases, or services.
**Solution:** Replace them with fake versions that return predictable results.

### Example: Mocking a Database

```python
from unittest.mock import Mock, patch

def test_with_mocked_db():
    """Test without hitting real database"""
    
    # Create a mock database
    mock_db = Mock()
    mock_db.get_student.return_value = {"id": 1, "name": "Mocked"}
    
    # Patch the real get_db function to return our mock
    with patch('app.get_db', return_value=mock_db):
        response = client.get('/students/1')
        assert response.status_code == 200
        assert response.json()["name"] == "Mocked"
```

### Example: Mocking HTTP Requests

```python
from unittest.mock import patch

def test_with_mocked_api():
    """Test code that calls external API"""
    
    mock_response = Mock()
    mock_response.json.return_value = {"weather": "sunny"}
    mock_response.status_code = 200
    
    with patch('requests.get', return_value=mock_response):
        result = get_weather("London")  # Your function
        assert result == "sunny"
```

---

## Chapter 6: Test Organization Best Practices

### Directory Structure

```
flask_app/
├── app.py
├── test_app.py          # Tests next to code (simple projects)
└── tests/
    ├── __init__.py
    ├── test_models.py   # Model tests
    ├── test_views.py    # View/route tests
    └── conftest.py      # Shared fixtures
```

### Naming Conventions

| What | Convention | Example |
|------|------------|---------|
| Test files | `test_*.py` or `*_test.py` | `test_app.py` |
| Test functions | `test_*` | `test_create_student` |
| Test classes | `Test*` | `TestStudentAPI` |

### The `conftest.py` File

Put shared fixtures here - they're available to all test files:

```python
# conftest.py
import pytest

@pytest.fixture
def sample_student():
    """Available to all tests in this directory"""
    return {
        "name": "Sample",
        "email": "sample@test.com",
        "role": "student"
    }

# In test_students.py
def test_something(sample_student):  # Fixture automatically injected
    assert sample_student["name"] == "Sample"
```

---

## Chapter 7: Running Tests

### pytest Command Reference

```bash
# Run all tests
pytest

# Run specific file
pytest test_app.py

# Run specific test
pytest test_app.py::test_create_student

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run with coverage report
pytest --cov=app --cov-report=html

# Run only failed tests from last run
pytest --lf
```

### Test Output Explained

```
pytest test_app.py -v

============================= test session starts ==============================
test_app.py::test_home_page PASSED                                     [ 33%]
test_app.py::test_api_students PASSED                                   [ 66%]
test_app.py::test_create_student FAILED                                [100%]

=================================== FAILURES ===================================
_____________________________ test_create_student ______________________________

    def test_create_student(client):
        response = client.post('/students', json={'name': 'Test'})
>       assert response.status_code == 201
E       assert 400 == 201
E        +  where 400 = <Response [400 BAD REQUEST]>.status_code

test_app.py:15: AssertionError
=========================== short test summary info ============================
FAILED test_app.py::test_create_student - assert 400 == 201
============================== 1 failed, 2 passed ==============================
```

---

## Quick Reference: Common Assertions

| What you want | pytest |
|---------------|--------|
| Equals | `assert a == b` |
| Not equals | `assert a != b` |
| True | `assert x` |
| False | `assert not x` |
| In list | `assert x in list` |
| Is None | `assert x is None` |
| Raises exception | `with pytest.raises(ValueError):` |
| Status code | `assert response.status_code == 200` |

---

## Exercise: Fix and Write Tests

### Task 1: Fix All Broken Tests

Open `test_example.py` and fix all three broken tests:
- `test_add()` — assert should check for 5, not 6
- `test_subtract()` — assert should check for 2, not 8  
- `test_multiply()` — assert should check for 20, not 25

Run `pytest test_example.py -v` until all tests pass.

### Task 2: Add a New Test

Add a `divide()` function and `test_divide()`:
1. Create `divide(a, b)` function that returns `a / b`
2. Create `test_divide()` that checks `divide(10, 2) == 5`
3. Run tests to verify it works

### Task 3: Break and Fix

1. Change one working assert to make it fail (e.g., change `== 5` to `== 99`)
2. Run pytest to see the error message
3. Fix it back so the test passes

---

## Summary: Testing Mindset

| Without Tests | With Tests |
|---------------|------------|
| "It works on my machine" | "CI/CD proves it works" |
| Afraid to refactor | Refactor with confidence |
| Manual testing every time | Automated, repeatable |
| Bugs found by users | Bugs caught before deploy |

**Golden Rule:** If it's worth writing, it's worth testing.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run pytest from project root, or set `PYTHONPATH` |
| `404` in Flask tests | Check URL path (leading `/` matters) |
| Database changes persist | Use mocking or in-memory DB |
| Tests too slow | Mock external services, use in-memory DB |
