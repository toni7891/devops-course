# Topic 6 — In-Class Final Exercise: REST API v1 (In-Memory)

**Time:** 15:30–16:30 (60 min)

---

## Objective

Build a complete CRUD REST API for tasks using only in-memory storage. Every endpoint uses decorators and returns a uniform response.

---

## Requirements

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tasks` | Return all tasks |
| GET | `/tasks/<id>` | Return one task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/<id>` | Update title or completed status |
| DELETE | `/tasks/<id>` | Delete a task |

### Task Model

```json
{
  "id": 1,
  "title": "Buy groceries",
  "completed": false
}
```

### Rules

1. `title` is required on POST — return 400 if missing
2. Return 404 with `{"success": false, "error": "Task not found"}` for unknown IDs
3. All routes use `@log_execution` and `@handle_errors`
4. POST uses `@validate_json` in addition
5. Every response follows `{"success": bool, "data": ...}` or `{"success": false, "error": "..."}`

### BONUS

Support filtering on GET /tasks:
```
GET /tasks?completed=true
GET /tasks?completed=false
```

---

## File Structure

```
6-REST-API-In-Memory/
  core/
    decorators.py
  main.py
```

---

## Testing Checklist

```bash
# Create tasks
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'

curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Write tests"}'

# Get all
curl http://localhost:5000/tasks

# Get one
curl http://localhost:5000/tasks/1

# Update
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete
curl -X DELETE http://localhost:5000/tasks/2

# 404 test
curl http://localhost:5000/tasks/999

# BONUS: filter
curl "http://localhost:5000/tasks?completed=true"
```
