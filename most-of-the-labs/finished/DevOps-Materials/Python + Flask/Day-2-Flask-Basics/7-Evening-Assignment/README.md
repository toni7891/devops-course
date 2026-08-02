# Topic 7 — Evening Assignment: Task Manager API v2 (Production Mindset)

**Difficulty:** Intermediate+

---

## Goal

Rebuild the in-class Task Manager API with proper separation of concerns, advanced validation, and production-ready error handling.

---

## Required Folder Structure

```
7-Evening-Assignment/
  app/
    routes.py      <- HTTP layer only — no business logic here
    services.py    <- all task logic lives here
    models.py      <- Task factory and validation
  core/
    decorators.py  <- log_execution, handle_errors, validate_json, measure_time (BONUS)
  main.py          <- creates Flask app and registers routes
```

---

## Requirements

### 1. Separation of Concerns

- `routes.py` — only HTTP: parse request, call service, return response
- `services.py` — only logic: create, read, update, delete, validate
- `models.py` — Task creation helper, field definitions

### 2. Service Functions

Implement all of these in `services.py`:

```python
def create_task(title: str) -> dict: ...
def get_tasks() -> dict: ...
def get_task(task_id: int) -> dict: ...
def update_task(task_id: int, fields: dict) -> dict: ...
def delete_task(task_id: int) -> dict: ...
```

Each returns `{"success": bool, "data": ...}` or `{"success": False, "error": {...}}`.

### 3. Unique ID Generator

Do not use a global counter in routes. Implement `generate_id()` in `models.py`.

### 4. Advanced Validation

Handle these cases explicitly:
- Empty string title (`""` or `"   "`)
- Duplicate title (case-insensitive)
- Missing title on POST

### 5. Uniform Error Format

All errors use this structure:

```json
{
  "success": false,
  "error": {
    "message": "Task not found",
    "code": 404
  }
}
```

### 6. Decorators

- `@log_execution` on every route
- `@handle_errors` on every route
- `@validate_json` on POST and PUT routes

---

## BONUS: Response Time Decorator

Add a `@measure_time` decorator to `core/decorators.py` that:
- Runs the route
- Adds an `X-Response-Time` header to the response (in milliseconds)

Example:
```
X-Response-Time: 1.23ms
```

This requires accessing the Flask response object after the route runs.

---

## Testing Checklist

```bash
# Normal flow
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'

curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Write tests"}'

curl http://localhost:5000/tasks
curl http://localhost:5000/tasks/1

curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

curl -X DELETE http://localhost:5000/tasks/2

# Validation errors
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": ""}'

curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'

# 404
curl http://localhost:5000/tasks/999
```
