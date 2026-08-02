# Topic 5 — Decorators + Uniform Response

**Time:** 14:30–15:30 (60 min)

---

## Objectives

- Reuse Day 1 decorators inside a Flask app
- Write a `@validate_json` decorator for POST/PUT routes
- Enforce a uniform response structure on every endpoint
- Understand decorator stacking order in Flask

---

## Topics

### 1. Bringing Day 1 Decorators In

The decorators from Day 1 (`@log_execution`, `@handle_errors`) work in Flask exactly as before — they wrap functions. The only difference is that our functions now return Flask responses.

**Key rule:** `@log_execution` always goes **above** `@handle_errors`.

```python
@app.route("/tasks", methods=["POST"])
@log_execution
@handle_errors
def create_task():
    ...
```

Execution order (outer → inner):
1. `log_execution` starts timing
2. `handle_errors` wraps in try/except
3. `create_task` runs
4. `handle_errors` catches any exception
5. `log_execution` logs duration

### 2. The Uniform Response Contract

Every endpoint in this course returns one of these shapes:

**Success:**
```json
{"success": true, "data": <any>}
```

**Failure:**
```json
{"success": false, "error": "<message>"}
```

This makes client-side handling predictable — always check `success` first.

### 3. `@validate_json` Decorator

Validates that the request has a JSON body before the route function runs:

```python
def validate_json(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not request.json:
            return jsonify({"success": False, "error": "JSON body required"}), 400
        return func(*args, **kwargs)
    return wrapper
```

Apply it to any route that expects a body:

```python
@app.route("/tasks", methods=["POST"])
@log_execution
@handle_errors
@validate_json
def create_task():
    ...
```

### 4. `@handle_errors` in Flask Context

The Day 1 version catches `requests` exceptions. For Flask routes we need a version that catches general exceptions and returns a proper JSON response:

```python
def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    return wrapper
```

---

## Exercise

### `app_with_decorators.py`

Take the `app.py` from Topic 4 and add:
1. A `core/decorators.py` with `log_execution`, `handle_errors`, `validate_json`
2. Apply all three decorators to `POST /tasks`
3. Apply `log_execution` + `handle_errors` to `GET /tasks`
4. Verify that hitting `/tasks` (POST) without a body returns the correct error

---

## Common Mistakes

- Stacking decorators in the wrong order (Flask's `@app.route` must always be outermost)
- `validate_json` accessing `request` outside of a request context — this is fine inside a route
- Returning a plain dict from `handle_errors` instead of a Flask `Response` — use `jsonify`
