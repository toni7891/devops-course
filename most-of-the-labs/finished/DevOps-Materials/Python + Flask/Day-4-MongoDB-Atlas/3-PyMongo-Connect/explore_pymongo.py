from pymongo import MongoClient

MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["task_manager"]
collection = db["tasks"]


def seed_tasks():
    titles = ["Write tests", "Deploy to staging", "Review pull request"]
    for title in titles:
        collection.insert_one({"title": title, "completed": False})
    print(f"Inserted {len(titles)} tasks")


def print_all_tasks():
    print("\nAll tasks:")
    for doc in collection.find():
        doc["_id"] = str(doc["_id"])
        print(f"  {doc}")


def find_by_title(title: str):
    doc = collection.find_one({"title": title})
    if doc:
        doc["_id"] = str(doc["_id"])
        print(f"\nFound: {doc}")
    else:
        print(f"\nNo task with title '{title}'")


def count_tasks():
    total = collection.count_documents({})
    print(f"\nTotal tasks in collection: {total}")


if __name__ == "__main__":
    seed_tasks()
    print_all_tasks()
    find_by_title("Write tests")
    count_tasks()
