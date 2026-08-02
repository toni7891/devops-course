from datetime import datetime, timezone


def doc_to_task(doc: dict) -> dict:
    task = {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "completed": doc["completed"],
    }
    # BONUS: include created_at if present
    if "created_at" in doc:
        task["created_at"] = doc["created_at"].isoformat()
    return task


def new_task_doc(title: str) -> dict:
    return {
        "title": title.strip(),
        "completed": False,
        "created_at": datetime.now(timezone.utc),  # BONUS
    }
