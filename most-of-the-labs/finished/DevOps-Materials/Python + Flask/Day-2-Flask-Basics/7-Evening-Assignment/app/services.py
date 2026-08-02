from app.models import make_task

_tasks: list[dict] = []


def _find(task_id: int) -> dict | None:
    return next((t for t in _tasks if t["id"] == task_id), None)


def _title_exists(title: str, exclude_id: int | None = None) -> bool:
    return any(
        t["title"].lower() == title.strip().lower()
        for t in _tasks
        if t["id"] != exclude_id
    )


def get_tasks(completed: bool | None = None) -> dict:
    if completed is not None:
        result = [t for t in _tasks if t["completed"] == completed]
    else:
        result = list(_tasks)
    return {"success": True, "data": result}


def get_task(task_id: int) -> dict:
    task = _find(task_id)
    if task is None:
        return {"success": False, "error": {"message": "Task not found", "code": 404}}
    return {"success": True, "data": task}


def create_task(title: str) -> dict:
    if not title or not title.strip():
        return {"success": False, "error": {"message": "title cannot be empty", "code": 400}}

    if _title_exists(title):
        return {"success": False, "error": {"message": "A task with this title already exists", "code": 409}}

    task = make_task(title)
    _tasks.append(task)
    return {"success": True, "data": task}


def update_task(task_id: int, fields: dict) -> dict:
    task = _find(task_id)
    if task is None:
        return {"success": False, "error": {"message": "Task not found", "code": 404}}

    if "title" in fields:
        new_title = fields["title"]
        if not new_title or not new_title.strip():
            return {"success": False, "error": {"message": "title cannot be empty", "code": 400}}
        if _title_exists(new_title, exclude_id=task_id):
            return {"success": False, "error": {"message": "A task with this title already exists", "code": 409}}
        task["title"] = new_title.strip()

    if "completed" in fields:
        task["completed"] = bool(fields["completed"])

    return {"success": True, "data": task}


def delete_task(task_id: int) -> dict:
    task = _find(task_id)
    if task is None:
        return {"success": False, "error": {"message": "Task not found", "code": 404}}
    _tasks.remove(task)
    return {"success": True, "data": {"deleted_id": task_id}}
