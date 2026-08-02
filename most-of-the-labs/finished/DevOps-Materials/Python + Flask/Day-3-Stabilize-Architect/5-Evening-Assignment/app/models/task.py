_store: list["Task"] = []
_next_id = 1


class Task:
    def __init__(self, title: str, task_id: int | None = None):
        self.id = task_id
        self.title = title
        self.completed = False

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "completed": self.completed}


def save_task(task: "Task") -> "Task":
    """Persist a task. Assigns an ID and appends if new; updates in-place if existing."""
    global _next_id
    existing = next((t for t in _store if t.id == task.id), None) if task.id else None
    if existing is None:
        task.id = _next_id
        _next_id += 1
        _store.append(task)
    return task


def load_tasks() -> list["Task"]:
    """Return all persisted tasks."""
    return list(_store)


def find_by_id(task_id: int) -> "Task | None":
    return next((t for t in _store if t.id == task_id), None)


def remove_task(task: "Task") -> None:
    _store.remove(task)
