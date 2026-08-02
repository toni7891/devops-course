# Flask Error Handling — Notes

## What Is a Global Error Handler?

A global error handler is a function registered with `@app.errorhandler` that Flask calls automatically when an error of a specific type occurs anywhere in the application — not just in a single route. Instead of each route needing its own try/except block for HTTP errors (like 404 or 405), the global handler intercepts them in one place and returns a consistent response. This is the right place to translate Flask's default HTML error pages into the JSON format our API clients expect.

---

## Code Example

```python
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": {"message": "Resource not found", "code": "NOT_FOUND"}
    }), 404


@app.errorhandler(Exception)
def handle_exception(error):
    if isinstance(error, HTTPException):
        return jsonify({
            "success": False,
            "error": {"message": error.description, "code": str(error.code)}
        }), error.code

    return jsonify({
        "success": False,
        "error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}
    }), 500
```

---

## When to Use Global Handlers

- When Flask itself raises the error (e.g., no route matched → 404, wrong method → 405)
- When you call `abort(404)` from inside a route and want a single centralized response format
- When you want to guarantee that no unhandled exception ever returns an HTML page to an API client

## When NOT to Use Global Handlers

- For business validation errors (missing title, wrong type) — return these directly from the route or service
- For external API failures — handle these with the `@handle_errors` decorator
