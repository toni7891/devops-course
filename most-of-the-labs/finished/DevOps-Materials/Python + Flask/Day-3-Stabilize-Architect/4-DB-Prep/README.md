# Topic 4 — Think Like a Database (DB Prep Refactor)

**Time:** 14:45–16:30 (105 min)

---

## Objective

Refactor the Task Manager so that every layer has a single clear responsibility — and so that swapping the in-memory store for SQLAlchemy on Day 4 requires changing **only** `models/task.py`, nothing else.

---

## The Core Idea

Right now, tasks are stored as plain dicts in a list. SQLAlchemy will store them as class instances in a database table. If routes and services talk to raw dicts today, we have to rewrite them tomorrow.

The fix: **introduce a Task class now**, and make services work against that class — not dicts.

---

## Target Structure

```
app/
  routes.py          ← HTTP only: parse request, call service, return jsonify
  services.py        ← logic only: validation, orchestration, no HTTP
  models/
    __init__.py
    task.py          ← Task class + factory
core/
  decorators.py
main.py
```

---

## Topics

### 1. Defining Task as a Class

```python
class Task:
    def __init__(self, task_id: int, title: str):
        self.id = task_id
        self.title = title
        self.completed = False

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "completed": self.completed}
```

`to_dict()` is the seam: routes call it to get JSON-serializable data. Tomorrow, SQLAlchemy models get the same method.

### 2. In-Memory Store in models/task.py

The storage lives next to the model — not as a global in `app.py`:

```python
_store: list[Task] = []
_next_id = 1

def find_all() -> list[Task]: ...
def find_by_id(task_id: int) -> Task | None: ...
def save(task: Task) -> Task: ...
def delete(task: Task) -> None: ...
```

### 3. Services Call the Model Layer

```python
# services.py
from app.models.task import Task, find_by_id, find_all, save, delete

def get_task(task_id: int) -> dict:
    task = find_by_id(task_id)
    if task is None:
        return {"success": False, "error": {"message": "Task not found", "code": "TASK_NOT_FOUND"}}
    return {"success": True, "data": task.to_dict()}
```

### 4. Routes Call Services Only

```python
# routes.py
@tasks_bp.route("/tasks/<int:task_id>")
def get_task(task_id):
    result = services.get_task(task_id)
    if not result["success"]:
        return jsonify(result), result["error"].get("status", 404)
    return jsonify(result)
```

---

## Why This Matters for Day 4

On Day 4, we replace the in-memory functions with SQLAlchemy queries:

| Today (in-memory) | Day 4 (SQLAlchemy) |
|-------------------|--------------------|
| `find_all()` returns a list | `Task.query.all()` returns a list |
| `save(task)` appends to list | `db.session.add(task); db.session.commit()` |
| `find_by_id(id)` searches list | `Task.query.get(id)` |

Services and routes stay **identical**.

---

## Deliverable

Refactored app with:
- `app/models/task.py` containing the `Task` class and in-memory store functions
- `app/services.py` using only model functions — no direct list access
- `app/routes.py` using only service functions — no direct model access
- `main.py` creating the Flask app and registering the Blueprint
