# Topic 2 — Flask Intro

**Time:** 10:15–11:15 (60 min)

---

## Objectives

- Understand what a web framework is and why we use one
- Create a minimal Flask application
- Define routes and return JSON responses
- Run a local development server

---

## Topics

### 1. What Is a Framework?

A framework gives you the scaffolding so you focus on **your** logic, not HTTP parsing.

| Without Flask | With Flask |
|---------------|------------|
| Parse raw TCP/HTTP | `@app.route("/")` |
| Parse headers manually | `request.headers` |
| Write response bytes | `jsonify({...})` |
| Route URLs to functions | Done automatically |

### 2. Minimal Flask App

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "API is running"})

if __name__ == "__main__":
    app.run(debug=True)
```

Key parts:
- `Flask(__name__)` — creates the app, `__name__` tells Flask where to find resources
- `@app.route("/")` — maps the URL `/` to the function below it
- `jsonify(...)` — serializes a dict to a proper JSON response with correct headers
- `debug=True` — auto-reloads on file save, shows errors in browser

### 3. Running the Server

```bash
python app.py
# OR
flask --app app run --debug
```

Server starts at `http://127.0.0.1:5000`

### 4. Testing Endpoints

```bash
# curl
curl http://localhost:5000/

# Or open in browser
```

---

## Exercises

### Guided: `hello_flask.py`

Build the minimal app above. Verify it returns JSON at `/`.

### Independent: `more_routes.py`

Add three more routes to the same app:

| Route | Returns |
|-------|---------|
| `/status` | `{"status": "ok", "version": "1.0"}` |
| `/time` | Current server time as ISO string |
| `/info` | App name, author, day number |

Each route must return valid JSON via `jsonify`.

---

## Common Mistakes

- Forgetting `jsonify` — returning a plain dict gives a `TypeError` in older Flask
- Two routes with the same path — Flask raises an `AssertionError`
- Not setting `debug=True` — changes don't reload automatically
- Calling `app.run()` outside `if __name__ == "__main__"` — causes issues when importing
