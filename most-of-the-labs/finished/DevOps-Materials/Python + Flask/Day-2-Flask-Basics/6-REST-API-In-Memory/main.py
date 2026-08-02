from flask import Flask, jsonify, request

from core.decorators import handle_errors, log_execution, validate_json

app = Flask(__name__)

tasks = []
next_id = 1


def find_task(task_id):
    return next((t for t in tasks if t["id"] == task_id), None)


@app.route("/tasks")
@log_execution
@handle_errors
def get_tasks():
    completed_filter = request.args.get("completed")

    if completed_filter is not None:
        want_completed = completed_filter.lower() == "true"
        filtered = [t for t in tasks if t["completed"] == want_completed]
        return jsonify({"success": True, "data": filtered})

    return jsonify({"success": True, "data": tasks})


@app.route("/tasks/<int:task_id>")
@log_execution
@handle_errors
def get_task(task_id):
    task = find_task(task_id)
    if task is None:
        return jsonify({"success": False, "error": "Task not found"}), 404
    return jsonify({"success": True, "data": task})


@app.route("/tasks", methods=["POST"])
@log_execution
@handle_errors
@validate_json
def create_task():
    global next_id

    body = request.json
    if not body.get("title"):
        return jsonify({"success": False, "error": "title is required"}), 400

    task = {
        "id": next_id,
        "title": body["title"],
        "completed": False,
    }
    tasks.append(task)
    next_id += 1

    return jsonify({"success": True, "data": task}), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
@log_execution
@handle_errors
@validate_json
def update_task(task_id):
    task = find_task(task_id)
    if task is None:
        return jsonify({"success": False, "error": "Task not found"}), 404

    body = request.json
    if "title" in body:
        task["title"] = body["title"]
    if "completed" in body:
        task["completed"] = bool(body["completed"])

    return jsonify({"success": True, "data": task})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@log_execution
@handle_errors
def delete_task(task_id):
    task = find_task(task_id)
    if task is None:
        return jsonify({"success": False, "error": "Task not found"}), 404

    tasks.remove(task)
    return jsonify({"success": True, "data": {"deleted_id": task_id}})


if __name__ == "__main__":
    app.run(debug=True)
