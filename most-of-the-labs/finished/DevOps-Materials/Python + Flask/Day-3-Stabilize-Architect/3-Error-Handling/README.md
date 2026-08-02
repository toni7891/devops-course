# Topic 3 — Flask Error Handling Deep Dive

**Time:** 13:30–14:45 (75 min)

---

## Objective

Understand how Flask handles HTTP errors internally, and register global error handlers so that consistent JSON responses are returned for any error — even ones not triggered by your code.

---

## Topics

### 1. How Flask Handles Errors Internally

When Flask cannot match a route, or when `abort()` is called, it raises an `HTTPException`. By default, Flask returns an HTML page — useless for an API.

```
GET /nonexistent  →  Flask raises 404 NotFound  →  HTML response (bad)
```

We want JSON instead.

### 2. The `abort()` Function

`abort()` raises an HTTP exception immediately, skipping the rest of the route:

```python
from flask import abort

@app.route("/tasks/<int:task_id>")
def get_task(task_id):
    task = find_task(task_id)
    if task is None:
        abort(404)          # raises NotFound, jumps to error handler
    return jsonify(task)
```

### 3. Global Error Handlers with `@app.errorhandler`

Register a handler for a specific HTTP status code:

```python
from flask import jsonify
from werkzeug.exceptions import HTTPException

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": {"message": "Resource not found", "code": "NOT_FOUND"}
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": {"message": "Bad request", "code": "BAD_REQUEST"}
    }), 400
```

### 4. Catch-All Handler

To return JSON for **any** unhandled exception:

```python
@app.errorhandler(Exception)
def handle_exception(error):
    if isinstance(error, HTTPException):
        return jsonify({
            "success": False,
            "error": {"message": error.description, "code": str(error.code)}
        }), error.code
    # Non-HTTP exceptions (bugs in your code)
    return jsonify({
        "success": False,
        "error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}
    }), 500
```

### 5. When to Use Global Handlers vs Per-Route Try/Except

| Scenario | Use |
|----------|-----|
| HTTP errors (404, 405, 422) | Global handler |
| Business logic errors (validation) | Per-route, return directly |
| Unexpected exceptions (bugs) | Global catch-all |
| External API failures | Per-route `handle_errors` decorator |

> Rule: global handlers are for HTTP-layer problems. Decorators are for business-layer problems.

---

## Deliverable

### `error_handling_notes.md`

Write a file in this folder that contains:

1. **What is a global error handler** — one paragraph in your own words
2. **Code example** — a working `@app.errorhandler(404)` and `@app.errorhandler(Exception)`
3. **When to use it** — 2-3 bullet points

### Implementation

Add at least one global handler to your Part 1 app (`2-Stabilize-API/app.py`):
- `404` — for unknown routes and missing resources
- `400` — for bad request format (Flask's default for malformed JSON)

---

## Exercise: `global_handlers.py`

A standalone Flask app demonstrating:

1. A route that uses `abort(404)` to trigger the global handler
2. A route that raises an unhandled exception (to test the catch-all)
3. All three handler registrations

Test it:
```bash
curl http://localhost:5000/missing         # triggers 404 handler
curl http://localhost:5000/crash           # triggers catch-all
curl http://localhost:5000/abort-demo/999  # triggers abort(404)
```
