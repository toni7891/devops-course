# Topic 4 — Task Manager API v1 (Final Project Layer 1)

**Time:** 13:30–14:30 (60 min)

---

## Objectives

- Start the multi-day final project
- Store data in memory (in-process list)
- Build `GET /tasks` and `POST /tasks`
- Understand the role of an auto-incrementing ID

---

## The Final Project

Every day adds a layer to the **Task Manager API**:

| Day | Layer |
|-----|-------|
| Day 2 | In-memory CRUD, single file |
| Day 3 | Blueprints, proper structure |
| Day 4 | Database persistence |
| Day 5 | Auth, deployment |

---

## Topics

### 1. In-Memory Storage

```python
tasks = []          # our "database" for today
next_id = 1         # auto-increment counter
```

This resets every time the server restarts — that is expected for now.

### 2. GET /tasks

Returns all tasks. Always succeeds (empty list is valid).

```python
@app.route("/tasks")
def get_tasks():
    return jsonify({"success": True, "data": tasks})
```

### 3. POST /tasks

Creates a new task. Must validate that `title` is present.

```python
@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    body = request.json
    if not body or not body.get("title"):
        return jsonify({"success": False, "error": "title is required"}), 400

    task = {"id": next_id, "title": body["title"], "completed": False}
    tasks.append(task)
    next_id += 1
    return jsonify({"success": True, "data": task}), 201
```

---

## Exercise

### Guided: `app.py`

Build the file step by step with the class:
1. Create the Flask app
2. Add in-memory storage
3. Implement `GET /tasks`
4. Implement `POST /tasks` with validation

Test with curl:
```bash
# Get all tasks (empty)
curl http://localhost:5000/tasks

# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'

# Get all tasks again
curl http://localhost:5000/tasks
```

---

## Discussion

- What happens to tasks when you restart the server?
- How would you persist them? (preview Day 4)
- What if two requests arrive at the same time — is the counter safe? (preview concurrency)
