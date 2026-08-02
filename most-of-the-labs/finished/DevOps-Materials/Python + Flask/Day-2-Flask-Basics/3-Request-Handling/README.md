# Topic 3 — Request Handling

**Time:** 11:15–12:30 (75 min)

---

## Objectives

- Read query parameters from the URL using `request.args`
- Read a JSON body from a POST request using `request.json`
- Return the correct HTTP status codes
- Handle missing/invalid input gracefully

---

## Topics

### 1. Query Parameters

Query params appear after `?` in the URL: `/search?name=Alice&limit=10`

```python
from flask import Flask, jsonify, request

@app.route("/search")
def search():
    name = request.args.get("name")        # None if missing
    name = request.args.get("name", "")   # default value
    return jsonify({"query": name})
```

### 2. Reading JSON Body

For POST/PUT requests that send a JSON body:

```python
@app.route("/echo", methods=["POST"])
def echo():
    body = request.json          # parsed dict, None if Content-Type is wrong
    return jsonify(body)
```

> Always check `if request.json is None` before using it.

### 3. HTTP Status Codes

```python
return jsonify({"error": "not found"}), 404
return jsonify({"data": result}), 200
return jsonify({"data": created}), 201   # resource created
return jsonify({"error": "bad input"}), 400
```

### 4. Specifying HTTP Methods

```python
@app.route("/echo", methods=["POST"])        # POST only
@app.route("/tasks", methods=["GET", "POST"]) # both
```

---

## Exercises

### Guided: `search_endpoint.py`

Build a `GET /search?name=...` endpoint:
- If `name` is provided, return `{"success": True, "query": name, "results": [...]}`
- If `name` is missing, return `{"success": False, "error": "name is required"}` with status 400

### Advanced: `echo_endpoint.py`

Build a `POST /echo` endpoint:
- Reads the JSON body
- Returns exactly what was sent, wrapped: `{"success": True, "echo": <body>}`
- If no body / not JSON, return `{"success": False, "error": "JSON body required"}` with 400

---

## Common Mistakes

- Using `request.args` for POST body (use `request.json` instead)
- Forgetting `methods=["POST"]` on a route — Flask defaults to GET only
- Not handling `None` from `request.json` — crashes with `TypeError`
- Not returning a status code — Flask defaults to 200, which can mislead clients
