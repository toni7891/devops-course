# Topic 6 — Connect Mongo to the Project + In-Class Final Exercise

**Time:** 14:30–16:30 (120 min)

---

## Part A: Refactor (14:30–15:30)

### Objective

Replace the in-memory store from Day 3 with MongoDB. Routes stay identical — only `services.py` changes.

### The Rule

```
routes.py  →  services.py  →  MongoDB collection
                ↑
       ONLY this layer touches the DB
```

### What Changes vs Day 3

| Day 3 | Day 4 |
|-------|-------|
| `from app.models.task import find_by_id, save_task...` | `from bson import ObjectId; collection.find_one(...)` |
| `Task` class, in-memory `_store` list | MongoDB document dict |
| `task.to_dict()` | `_doc_to_task(doc)` helper |
| `task.id` is an int | `task["id"]` is a string (from ObjectId) |

### Key Structural Decision

`routes.py` uses `task["id"]` everywhere (string). That is the only change clients see — IDs are now 24-character hex strings instead of integers.

---

## Part B: In-Class Final Exercise — Cloud Database API (15:30–16:30)

### Requirements

- Full CRUD working against Atlas — no local data
- All data persists across server restarts
- ObjectId stored in Mongo, returned as `string` in JSON
- Uniform response: `{"success": bool, "data": ...}` or `{"success": false, "error": {...}}`
- All decorators in place (`@log_execution`, `@handle_errors`, `@validate_json`)
- Validation: title required + min 3 chars, completed must be boolean

### File Structure

```
6-Project-Refactor/
  core/
    decorators.py
  app/
    routes.py
    services.py
  main.py
```

### Test Checklist

```bash
# Create
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Persist this"}'

# Get all (survives restart — data is in Atlas)
curl http://localhost:5000/tasks

# Get one (use the id from the create response)
curl http://localhost:5000/tasks/<id>

# Update
curl -X PUT http://localhost:5000/tasks/<id> \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete
curl -X DELETE http://localhost:5000/tasks/<id>

# Validation errors
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "ab"}'

# 404
curl http://localhost:5000/tasks/000000000000000000000000
```
