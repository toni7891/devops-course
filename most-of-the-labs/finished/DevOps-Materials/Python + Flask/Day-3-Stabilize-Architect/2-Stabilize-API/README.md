# Topic 2 — Stabilize Your API

**Time:** 10:00–12:30 (150 min)

---

## Objective

Upgrade the Day 2 Task Manager API to handle every realistic failure case with consistent, professional responses.

---

## Requirements

### Endpoints (same as Day 2, stricter behavior)

| Method | Path | Notes |
|--------|------|-------|
| GET | `/tasks` | Always succeeds |
| GET | `/tasks/<id>` | 404 if not found |
| POST | `/tasks` | Validate title |
| PUT | `/tasks/<id>` | 404 if not found, 400 if no valid fields |
| DELETE | `/tasks/<id>` | 404 if not found |

---

### Validation Rules

| Field | Rule | Error Code |
|-------|------|------------|
| `title` | Required | `TITLE_REQUIRED` |
| `title` | Minimum 3 characters | `TITLE_TOO_SHORT` |
| `completed` | Must be boolean (`true`/`false`) | `INVALID_COMPLETED` |

---

### Error Response Format

```json
{
  "success": false,
  "error": {
    "message": "Title must be at least 3 characters",
    "code": "TITLE_TOO_SHORT"
  }
}
```

Note: `code` is a **string constant**, not an HTTP integer.

---

### Edge Cases (students commonly miss these)

| Scenario | Expected behavior |
|----------|-------------------|
| `GET /tasks/999` | 404 + `TASK_NOT_FOUND` |
| `PUT /tasks/1` with `{}` | 400 + `NO_UPDATE_FIELDS` |
| `DELETE /tasks/999` | 404 + `TASK_NOT_FOUND` |
| `POST /tasks` with empty body | 400 + `JSON_REQUIRED` |
| `POST /tasks` with `{"title": "ab"}` | 400 + `TITLE_TOO_SHORT` |
| `PUT /tasks/1` with `{"completed": "yes"}` | 400 + `INVALID_COMPLETED` |

---

### Required Decorators

- `@handle_errors` — on every route
- `@validate_json` — on POST and PUT

---

### Uniform Success Response

```json
{
  "success": true,
  "data": { ... }
}
```

---

## Deliverable

1. All endpoints passing the test checklist below
2. A Postman collection (exported as `tasks_collection.json`) that demonstrates every CRUD operation and at least 3 error cases

---

## Instructor Test Checklist

```bash
# Create — valid
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'

# Create — title too short
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "ab"}'

# Create — missing title
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{}'

# Create — empty body
curl -X POST http://localhost:5000/tasks

# Get all
curl http://localhost:5000/tasks

# Get one — exists
curl http://localhost:5000/tasks/1

# Get one — missing
curl http://localhost:5000/tasks/999

# Update — valid
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Update — bad completed type
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": "yes"}'

# Update — no fields
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{}'

# Delete — exists
curl -X DELETE http://localhost:5000/tasks/1

# Delete — already gone
curl -X DELETE http://localhost:5000/tasks/1
```
