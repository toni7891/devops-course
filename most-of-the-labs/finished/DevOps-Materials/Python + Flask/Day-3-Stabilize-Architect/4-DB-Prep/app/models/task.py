_store: list["Task"] = []
_next_id = 1


class Task:
    def __init__(self, task_id: int, title: str):
        self.id = task_id
        self.title = title
        self.completed = False

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "completed": self.completed}


# ── in-memory store functions (same interface as Day 4 SQLAlchemy) ────────────

def find_all() -> list[Task]:
    return list(_store)


def find_by_id(task_id: int) -> Task | None:
    return next((t for t in _store if t.id == task_id), None)


def save(task: Task) -> Task:
    global _next_id
    if task.id is None:
        task.id = _next_id
        _next_id += 1
        _store.append(task)
    return task


def delete(task: Task) -> None:
    _store.remove(task)
