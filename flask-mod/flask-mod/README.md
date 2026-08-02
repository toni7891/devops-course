# Flask Task API (my_API_app)

This repository contains a small Flask-based Task Management API used for learning and exercises.

**Contents**
- `my_API_app/` — main application package
  - `app.py` — application factory / entry point
  - `database.py` — MongoDB connection helper (provides `get_collection`)
  - `routes.py` — Flask route handlers for the API
  - `models.py` — business logic / data access functions (uses `get_collection`)
  - `errors.py` — centralized error handlers
  - `static/` — static assets (CSS)
  - `templates/` — HTML templates (optional UI)
- `tests/` — pytest tests
- `todo_p1.py`, `todo_p2.py`, `prac_lessons/` — practice files and labs

Project structure (high level):
```
README.md
todo_p1.py
todo_p2.py
my_API_app/
  app.py
  database.py
  errors.py
  models.py
  routes.py
  requirements.txt
  static/
    style.css
  templates/
    index.html
tests/
  conftest.py
  test_task_app.py
prac_lessons/
  lab1.py
  lab2.py
  lesson_prac1.py
```

**What this app does**
- Provides CRUD endpoints to manage tasks stored in a MongoDB collection called `data`.
- Supports multiple named collections (namespaces) via a `collections` collection.
- Validates input and returns JSON errors using `werkzeug` exceptions.

Key behavior implemented in `my_API_app/models.py`:
- List all tasks and convert Mongo ObjectIds to strings for JSON responses.
- Create/delete collections and cascade-delete tasks for a collection.
- Create tasks (global or scoped to a collection) with `title` (string) and optional `completed` (boolean).
- Fetch, edit, and delete single tasks by ObjectId string; raises `NotFound` when missing.
- Robust input validation: non-empty titles, correct types, and clear error codes.

Getting started
---------------
1. Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r my_API_app/requirements.txt
```

3. Configure MongoDB
- `my_API_app/database.py` expects a Mongo connection. Set environment variables if used (e.g. `MONGODB_URI`) or update `database.py` to point to your local Mongo.

4. Run the app locally:

```bash
python my_API_app/app.py
```

5. Run tests:

```bash
pytest -q
```

API Summary
-----------
- `GET /tasks` — list all tasks
- `POST /tasks` — create a task: `{"title": "Buy milk"}`
- `GET /tasks/<id>` — get task by id
- `PUT /tasks/<id>` — update task (title and/or completed)
- `DELETE /tasks/<id>` — delete task by id

Collection-specific endpoints (if implemented in `routes.py`):
- `GET /collections` — list collection names
- `POST /collections` — create collection `{ "collection": "work" }`
- `DELETE /collections/<name>` — delete a collection and its tasks
- `GET /collections/<name>/tasks` — tasks for a collection
- `POST /collections/<name>/tasks` — create task in a collection

Notes & Next steps
------------------
- `models.py` currently uses `bson.ObjectId` and raises `werkzeug` exceptions; ensure your `database.py` returns proper PyMongo collections.


File references
---------------
- See `my_API_app/models.py` for data validation and operations.
- See `my_API_app/routes.py` for the exact route definitions and payload expectations.
