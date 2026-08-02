from flask import Blueprint, jsonify, request

from app import services
from core.decorators import handle_errors, log_execution, validate_json

tasks_bp = Blueprint("tasks", __name__)


def _error_status(result: dict) -> int:
    return result["error"].get("code", 500)


@tasks_bp.route("/tasks")
@log_execution
@handle_errors
def get_tasks():
    completed_param = request.args.get("completed")
    completed_filter = None
    if completed_param is not None:
        completed_filter = completed_param.lower() == "true"

    result = services.get_tasks(completed=completed_filter)
    return jsonify(result)


@tasks_bp.route("/tasks/<int:task_id>")
@log_execution
@handle_errors
def get_task(task_id):
    result = services.get_task(task_id)
    if not result["success"]:
        return jsonify(result), _error_status(result)
    return jsonify(result)


@tasks_bp.route("/tasks", methods=["POST"])
@log_execution
@handle_errors
@validate_json
def create_task():
    title = request.json.get("title", "")
    result = services.create_task(title)
    if not result["success"]:
        return jsonify(result), _error_status(result)
    return jsonify(result), 201


@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@log_execution
@handle_errors
@validate_json
def update_task(task_id):
    result = services.update_task(task_id, request.json)
    if not result["success"]:
        return jsonify(result), _error_status(result)
    return jsonify(result)


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@log_execution
@handle_errors
def delete_task(task_id):
    result = services.delete_task(task_id)
    if not result["success"]:
        return jsonify(result), _error_status(result)
    return jsonify(result)
