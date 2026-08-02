from bson import ObjectId
from bson.errors import InvalidId

from app.models.task import doc_to_task, new_task_doc
from db.mongo_client import get_collection


def _col():
    return get_collection("tasks")


def _to_oid(task_id: str) -> ObjectId | None:
    try:
        return ObjectId(task_id)
    except InvalidId:
        return None


def _err(message: str, code: str, status: int) -> dict:
    return {"success": False, "error": {"message": message, "code": code, "status": status}}


def _validate_title(title) -> dict | None:
    if title is None or not isinstance(title, str) or not title.strip():
        return _err("title is required", "TITLE_REQUIRED", 400)
    if len(title.strip()) < 3:
        return _err("title must be at least 3 characters", "TITLE_TOO_SHORT", 400)
    return None


def get_tasks() -> dict:
    tasks = [doc_to_task(doc) for doc in _col().find()]
    return {"success": True, "data": tasks}


def get_task(task_id: str) -> dict:
    oid = _to_oid(task_id)
    if oid is None:
        return _err("Invalid task id", "INVALID_ID", 400)
    doc = _col().find_one({"_id": oid})
    if doc is None:
        return _err("Task not found", "TASK_NOT_FOUND", 404)
    return {"success": True, "data": doc_to_task(doc)}


def create_task(title: str) -> dict:
    err = _validate_title(title)
    if err:
        return err
    doc = new_task_doc(title)
    result = _col().insert_one(doc)
    doc["_id"] = result.inserted_id
    return {"success": True, "data": doc_to_task(doc)}


def update_task(task_id: str, fields: dict) -> dict:
    oid = _to_oid(task_id)
    if oid is None:
        return _err("Invalid task id", "INVALID_ID", 400)

    updates = {}
    if "title" in fields:
        err = _validate_title(fields["title"])
        if err:
            return err
        updates["title"] = fields["title"].strip()

    if "completed" in fields:
        if not isinstance(fields["completed"], bool):
            return _err("completed must be a boolean", "INVALID_COMPLETED", 400)
        updates["completed"] = fields["completed"]

    if not updates:
        return _err("No valid fields provided", "NO_UPDATE_FIELDS", 400)

    result = _col().update_one({"_id": oid}, {"$set": updates})
    if result.matched_count == 0:
        return _err("Task not found", "TASK_NOT_FOUND", 404)

    doc = _col().find_one({"_id": oid})
    return {"success": True, "data": doc_to_task(doc)}


def delete_task(task_id: str) -> dict:
    oid = _to_oid(task_id)
    if oid is None:
        return _err("Invalid task id", "INVALID_ID", 400)
    result = _col().delete_one({"_id": oid})
    if result.deleted_count == 0:
        return _err("Task not found", "TASK_NOT_FOUND", 404)
    return {"success": True, "data": {"deleted_id": task_id}}
