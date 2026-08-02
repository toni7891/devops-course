from flask import Flask, jsonify, request

from core.decorators import handle_errors, log_execution, validate_json

app = Flask(__name__)

tasks: list[dict] = []
_next_id = 1


# ── helpers ──────────────────────────────────────────────────────────────────

def _find(task_id: int) -> dict | None:
    return next((t for t in tasks if t["id"] == task_id), None)


def _error(message: str, code: str, status: int):
    return jsonify({"success": False, "error": {"message": message, "code": code}}), status


def _validate_title(title) -> tuple[str, str] | None:
    """Returns (message, code) if invalid, else None."""
    if title is None:
        return "title is required", "TITLE_REQUIRED"
    if not isinstance(title, str) or not title.strip():
        return "title must be a non-empty string", "TITLE_REQUIRED"
    if len(title.strip()) < 3:
        return "title must be at least 3 characters", "TITLE_TOO_SHORT"
    return None


def _validate_completed(completed) -> tuple[str, str] | None:
    if not isinstance(completed, bool):
        return "completed must be a boolean", "INVALID_COMPLETED"
    return None


# ── routes ────────────────────────────────────────────────────────────────────

@app.route("/tasks")
@log_execution
@handle_errors
def get_tasks():
    return jsonify({"success": True, "data": tasks})


@app.route("/tasks/<int:task_id>")
@log_execution
@handle_errors
def get_task(task_id):
    task = _find(task_id)
    if task is None:
        return _error("Task not found", "TASK_NOT_FOUND", 404)
    return jsonify({"success": True, "data": task})


@app.route("/tasks", methods=["POST"])
@log_execution
@handle_errors
@validate_json
def create_task():
    global _next_id
    body = request.json

    err = _validate_title(body.get("title"))
    if err:
        return _error(*err, 400)

    task = {"id": _next_id, "title": body["title"].strip(), "completed": False}
    tasks.append(task)
    _next_id += 1
    return jsonify({"success": True, "data": task}), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
@log_execution
@handle_errors
@validate_json
def update_task(task_id):
    task = _find(task_id)
    if task is None:
        return _error("Task not found", "TASK_NOT_FOUND", 404)

    body = request.json
    updated = False

    if "title" in body:
        err = _validate_title(body["title"])
        if err:
            return _error(*err, 400)
        task["title"] = body["title"].strip()
        updated = True

    if "completed" in body:
        err = _validate_completed(body["completed"])
        if err:
            return _error(*err, 400)
        task["completed"] = body["completed"]
        updated = True

    if not updated:
        return _error("No valid fields provided", "NO_UPDATE_FIELDS", 400)

    return jsonify({"success": True, "data": task})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@log_execution
@handle_errors
def delete_task(task_id):
    task = _find(task_id)
    if task is None:
        return _error("Task not found", "TASK_NOT_FOUND", 404)
    tasks.remove(task)
    return jsonify({"success": True, "data": {"deleted_id": task_id}})


if __name__ == "__main__":
    app.run(debug=True)
