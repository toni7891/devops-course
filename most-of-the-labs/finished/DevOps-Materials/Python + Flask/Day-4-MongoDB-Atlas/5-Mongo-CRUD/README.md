# Topic 5 — MongoDB CRUD Outside Flask

**Time:** 13:30–14:30 (60 min)

---

## Objective

Build all five CRUD operations against MongoDB using PyMongo directly — no Flask involved yet. Understand ObjectId handling before it is needed inside the API.

---

## Topics

### 1. insert_one — Create

```python
result = collection.insert_one({
    "title": "Buy groceries",
    "completed": False
})
print(result.inserted_id)   # ObjectId('...')
```

### 2. find / find_one — Read

```python
# All documents
docs = list(collection.find())

# With a filter
doc = collection.find_one({"title": "Buy groceries"})

# With projection (exclude _id)
docs = list(collection.find({}, {"_id": 0}))
```

### 3. update_one — Update

```python
from bson import ObjectId

collection.update_one(
    {"_id": ObjectId(task_id_string)},
    {"$set": {"completed": True}}
)
```

`$set` updates only the specified fields. Without it, the whole document is replaced.

### 4. delete_one — Delete

```python
from bson import ObjectId

result = collection.delete_one({"_id": ObjectId(task_id_string)})
print(result.deleted_count)   # 1 if found, 0 if not
```

### 5. ObjectId — The Critical Detail

MongoDB stores IDs as `ObjectId` objects, not strings. You must convert in both directions:

```python
from bson import ObjectId

# Mongo document → API response (ObjectId → string)
doc["_id"] = str(doc["_id"])

# API request → Mongo query (string → ObjectId)
query_id = ObjectId(task_id_string)
```

Always wrap `ObjectId(string)` in a try/except — an invalid string raises `bson.errors.InvalidId`.

---

## Exercise: `mongo_crud.py`

Build five standalone functions (no Flask):

```python
def create_task(title: str) -> dict: ...        # insert_one, return task with id as str
def get_tasks() -> list[dict]: ...              # find all, convert _id
def get_task_by_id(task_id: str) -> dict|None:...  # find_one by ObjectId
def update_task(task_id: str, fields: dict) -> bool: ...  # update_one, return True/False
def delete_task(task_id: str) -> bool: ...      # delete_one, return True if deleted
```

Then a `main()` that demonstrates all five in sequence and prints results.

---

## Common Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Query with string `_id` | No results (silent) | Wrap in `ObjectId(...)` |
| Return doc without converting `_id` | `TypeError: ObjectId is not JSON serializable` | `doc["_id"] = str(doc["_id"])` |
| Use `$set` incorrectly | Whole document replaced | Always use `{"$set": {...}}` |
| `delete_one` on missing id | No error, `deleted_count == 0` | Check `result.deleted_count` |
