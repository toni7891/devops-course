_next_id = 1


def generate_id() -> int:
    global _next_id
    task_id = _next_id
    _next_id += 1
    return task_id


def make_task(title: str) -> dict:
    return {
        "id": generate_id(),
        "title": title.strip(),
        "completed": False,
    }
