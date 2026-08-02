# Topic 3 — Connecting with PyMongo

**Time:** 11:00–12:00 (60 min)

---

## Objectives

- Install PyMongo
- Understand the client → database → collection hierarchy
- Insert a document and see it appear in the Atlas UI
- Retrieve documents with `find` and `find_one`

---

## Install

```bash
pip install pymongo
```

---

## Topics

### 1. The PyMongo Hierarchy

```
MongoClient          ← connection to the Atlas cluster
  └── database       ← logical grouping (like a "schema")
        └── collection  ← where documents live (like a "table")
              └── document  ← a single record (like a "row")
```

```python
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client["task_manager"]        # creates the DB if it does not exist
collection = db["tasks"]           # creates the collection if it does not exist
```

> MongoDB creates databases and collections lazily — they appear in Atlas only after the first document is inserted.

### 2. Inserting a Document

```python
result = collection.insert_one({"title": "Buy groceries", "completed": False})
print(result.inserted_id)          # ObjectId('...')
```

The `_id` field is added automatically by MongoDB. It is a `bson.ObjectId` object — not a string.

### 3. Finding Documents

```python
# Find all
for doc in collection.find():
    print(doc)

# Find with a filter
doc = collection.find_one({"title": "Buy groceries"})
print(doc)
```

### 4. The `_id` Field

Every MongoDB document has an `_id` of type `ObjectId`. It looks like:
```
ObjectId('6630f1a2b3c4d5e6f7a8b9c0')
```

To use it as a string (e.g., in a JSON response):
```python
from bson import ObjectId

doc["_id"] = str(doc["_id"])
```

To query by `_id`, you must convert back:
```python
from bson import ObjectId

doc = collection.find_one({"_id": ObjectId("6630f1a2b3c4d5e6f7a8b9c0")})
```

---

## Guided Exercise: `first_connection.py`

Build step by step with the class:
1. Connect to Atlas
2. Get the `task_manager` database and `tasks` collection
3. Insert a task document
4. Find all tasks and print them
5. Open Atlas UI → Collections → verify the document appears

---

## Independent Exercise: `explore_pymongo.py`

Using the same collection:
1. Insert three tasks with different titles
2. Find and print all tasks (with `_id` converted to string)
3. Find only one task by title using `find_one`
4. Count how many tasks are in the collection: `collection.count_documents({})`
