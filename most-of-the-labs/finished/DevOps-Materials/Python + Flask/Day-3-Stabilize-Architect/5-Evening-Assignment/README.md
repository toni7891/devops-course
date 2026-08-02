# Topic 5 — Evening Assignment: Pre-Database Refactor

**Difficulty:** Advanced

---

## Goal

Eliminate the global list entirely. Build a storage abstraction layer that is shaped like a database repository — so that tomorrow's SQLAlchemy migration is a find-and-replace, not a rewrite.

---

## Required Structure

```
5-Evening-Assignment/
  app/
    routes.py          ← HTTP only
    services.py        ← logic only
    models/
      __init__.py
      task.py          ← Task class + to_dict()
    repository/
      __init__.py
      task_repo.py     ← BONUS: repository pattern
  core/
    decorators.py
  main.py
```

---

## Requirements

### 1. No Global List in Routes or Services

Every operation must go through the service layer. Routes never touch storage directly.

### 2. Service Functions

All five must exist in `services.py`:

```python
def create_task(title: str) -> dict: ...
def get_tasks() -> dict: ...
def get_task(task_id: int) -> dict: ...
def update_task(task_id: int, fields: dict) -> dict: ...
def delete_task(task_id: int) -> dict: ...
```

### 3. Storage Abstraction

Add these two functions (still in-memory, but shaped like persistence):

```python
def save_task(task: Task) -> Task:
    """Persist a task. Creates if new, updates if existing."""
    ...

def load_tasks() -> list[Task]:
    """Load all tasks from storage."""
    ...
```

These functions live in `app/models/task.py`. Services call them instead of manipulating a list directly.

### 4. Validation

Same rules as Part 1 (Topic 2):
- `title`: required, minimum 3 characters → `TITLE_REQUIRED`, `TITLE_TOO_SHORT`
- `completed`: must be boolean → `INVALID_COMPLETED`
- PUT with no valid fields → `NO_UPDATE_FIELDS`

### 5. Error Format

```json
{
  "success": false,
  "error": {
    "message": "Task not found",
    "code": "TASK_NOT_FOUND"
  }
}
```

### 6. Decorators

- `@log_execution` + `@handle_errors` on every route
- `@validate_json` on POST and PUT

### 7. Global Error Handlers

Register at minimum:
- `404` handler
- Generic `Exception` catch-all

---

## BONUS: Repository Pattern (`app/repository/task_repo.py`)

Build a `TaskRepository` class that wraps all storage operations:

```python
class TaskRepository:
    def find_all(self) -> list[Task]: ...
    def find_by_id(self, task_id: int) -> Task | None: ...
    def save(self, task: Task) -> Task: ...
    def delete(self, task: Task) -> None: ...
```

- Services import a single instance: `repo = TaskRepository()`
- The repo holds the in-memory list privately: `self._store`
- On Day 4, this class is replaced with SQLAlchemy queries — services change nothing

---

## Why the Repository Pattern?

| Without repo | With repo |
|--------------|-----------|
| Services know about lists | Services know about tasks |
| Changing storage = rewriting services | Changing storage = rewriting repo only |
| Hard to test services in isolation | Easy to inject a fake repo |

---

## Testing Checklist

```bash
# Full CRUD
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Read the docs"}'

curl http://localhost:5000/tasks
curl http://localhost:5000/tasks/1

curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

curl -X DELETE http://localhost:5000/tasks/1

# Validation
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "ab"}'

curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": "maybe"}'

# 404 via global handler
curl http://localhost:5000/nonexistent-route
```
