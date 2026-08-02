from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
collection = client["task_manager"]["tasks"]


def _doc_to_task(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


def create_task(title: str) -> dict:
    doc = {"title": title, "completed": False}
    result = collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return doc


def get_tasks() -> list[dict]:
    return [_doc_to_task(doc) for doc in collection.find()]


def get_task_by_id(task_id: str) -> dict | None:
    try:
        doc = collection.find_one({"_id": ObjectId(task_id)})
    except InvalidId:
        return None
    if doc is None:
        return None
    return _doc_to_task(doc)


def update_task(task_id: str, fields: dict) -> bool:
    try:
        result = collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": fields}
        )
    except InvalidId:
        return False
    return result.matched_count > 0


def delete_task(task_id: str) -> bool:
    try:
        result = collection.delete_one({"_id": ObjectId(task_id)})
    except InvalidId:
        return False
    return result.deleted_count > 0


def main():
    print("=== MongoDB CRUD Demo ===\n")

    # Create
    task = create_task("Buy groceries")
    print(f"Created: {task}")
    task_id = task["id"]

    task2 = create_task("Write tests")
    print(f"Created: {task2}")

    # Read all
    print(f"\nAll tasks ({len(get_tasks())} total):")
    for t in get_tasks():
        print(f"  {t}")

    # Read one
    found = get_task_by_id(task_id)
    print(f"\nFound by id: {found}")

    not_found = get_task_by_id("000000000000000000000000")
    print(f"Not found: {not_found}")

    # Update
    updated = update_task(task_id, {"completed": True})
    print(f"\nUpdated (should be True): {updated}")
    print(f"After update: {get_task_by_id(task_id)}")

    # Delete
    deleted = delete_task(task_id)
    print(f"\nDeleted (should be True): {deleted}")
    deleted_again = delete_task(task_id)
    print(f"Delete again (should be False): {deleted_again}")

    print(f"\nRemaining tasks: {len(get_tasks())}")


if __name__ == "__main__":
    main()
