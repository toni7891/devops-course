# BONUS: Repository Pattern
#
# This class is the single point of contact between services and storage.
# On Day 4, replace the body of each method with SQLAlchemy calls.
# Services import `repo` and never change.

from app.models.task import Task


class TaskRepository:
    def __init__(self):
        self._store: list[Task] = []
        self._next_id = 1

    def find_all(self) -> list[Task]:
        return list(self._store)

    def find_by_id(self, task_id: int) -> Task | None:
        return next((t for t in self._store if t.id == task_id), None)

    def save(self, task: Task) -> Task:
        existing = self.find_by_id(task.id) if task.id else None
        if existing is None:
            task.id = self._next_id
            self._next_id += 1
            self._store.append(task)
        return task

    def delete(self, task: Task) -> None:
        self._store.remove(task)


# Single shared instance — services import this object directly.
# On Day 4: swap for a SQLAlchemy-backed implementation of the same interface.
repo = TaskRepository()
