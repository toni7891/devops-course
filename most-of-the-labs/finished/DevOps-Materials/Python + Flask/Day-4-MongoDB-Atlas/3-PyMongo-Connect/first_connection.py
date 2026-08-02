from pymongo import MongoClient

MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["task_manager"]
collection = db["tasks"]


def insert_task(title: str) -> str:
    doc = {"title": title, "completed": False}
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def get_all_tasks() -> list[dict]:
    tasks = []
    for doc in collection.find():
        doc["_id"] = str(doc["_id"])
        tasks.append(doc)
    return tasks


if __name__ == "__main__":
    inserted_id = insert_task("Buy groceries")
    print(f"Inserted task with id: {inserted_id}")

    print("\nAll tasks in collection:")
    for task in get_all_tasks():
        print(f"  {task}")
