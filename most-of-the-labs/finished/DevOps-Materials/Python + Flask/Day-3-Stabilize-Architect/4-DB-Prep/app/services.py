from app.models.task import Task, delete, find_all, find_by_id, save


def _err(message: str, code: str, status: int) -> dict:
    return {"success": False, "error": {"message": message, "code": code, "status": status}}


def _validate_title(title) -> dict | None:
    if title is None or not isinstance(title, str) or not title.strip():
        return _err("title is required", "TITLE_REQUIRED", 400)
    if len(title.strip()) < 3:
        return _err("title must be at least 3 characters", "TITLE_TOO_SHORT", 400)
    return None


def get_tasks() -> dict:
    return {"success": True, "data": [t.to_dict() for t in find_all()]}


def get_task(task_id: int) -> dict:
    task = find_by_id(task_id)
    if task is None:
        return _err("Task not found", "TASK_NOT_FOUND", 404)
    return {"success": True, "data": task.to_dict()}


def create_task(title: str) -> dict:
    err = _validate_title(title)
    if err:
        return err

    task = Task(task_id=None, title=title.strip())
    save(task)
    return {"success": True, "data": task.to_dict()}


def update_task(task_id: int, fields: dict) -> dict:
    task = find_by_id(task_id)
    if task is None:
        return _err("Task not found", "TASK_NOT_FOUND", 404)

    updated = False

    if "title" in fields:
        err = _validate_title(fields["title"])
        if err:
            return err
        task.title = fields["title"].strip()
        updated = True

    if "completed" in fields:
        if not isinstance(fields["completed"], bool):
            return _err("completed must be a boolean", "INVALID_COMPLETED", 400)
        task.completed = fields["completed"]
        updated = True

    if not updated:
        return _err("No valid fields provided", "NO_UPDATE_FIELDS", 400)

    return {"success": True, "data": task.to_dict()}


def delete_task(task_id: int) -> dict:
    task = find_by_id(task_id)
    if task is None:
        return _err("Task not found", "TASK_NOT_FOUND", 404)
    delete(task)
    return {"success": True, "data": {"deleted_id": task_id}}
