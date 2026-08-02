# Topic 7 — Evening Assignment: Production Mongo Integration

**Difficulty:** Advanced

---

## Goal

Harden the MongoDB integration for production: no hardcoded secrets, connection retry on startup, isolated DB client module, and proper error handling when the database is unreachable.

---

## Required Structure

```
7-Evening-Assignment/
  db/
    mongo_client.py    ← single MongoClient, reads MONGO_URI from ENV
  app/
    routes.py          ← HTTP only, identical to Topic 6
    services.py        ← imports from db/ only — no direct Mongo imports elsewhere
    models/
      task.py          ← document helper (to_dict, doc_to_task)
  core/
    decorators.py
  main.py
  .env.example         ← MONGO_URI=mongodb+srv://...
```

---

## Requirements

### 1. Separate Connection File (`db/mongo_client.py`)

- One `MongoClient` instance shared across the app
- Reads the connection string from the `MONGO_URI` environment variable
- Uses `python-dotenv` to load `.env` automatically
- Raises a clear error if `MONGO_URI` is not set

### 2. No Hardcoded Connection Strings

No `.py` file may contain a literal `mongodb+srv://` string. All connection strings come from ENV.

### 3. Connection Retry on Startup

When the app starts, attempt to ping Atlas. If it fails, retry up to `MAX_RETRIES = 2` times with a 1-second sleep between attempts. If all retries fail, print a clear error and exit.

### 4. `services.py` Is the Only Importer of `db/`

```python
# Allowed in services.py:
from db.mongo_client import get_collection

# NOT allowed in routes.py or main.py:
from db.mongo_client import ...
```

### 5. Same CRUD + Validation as Topic 6

All five service functions, same validation rules, same error format.

### 6. Decorators

`@log_execution` + `@handle_errors` on every route, `@validate_json` on POST/PUT.

---

## BONUS: `created_at` Timestamp

Add a `created_at` field to every task document at creation time:

```python
from datetime import datetime, timezone

doc = {
    "title": title.strip(),
    "completed": False,
    "created_at": datetime.now(timezone.utc)
}
```

- Store as a native Python `datetime` (MongoDB handles it as BSON Date)
- Return as an ISO 8601 string in the API response
- Include in `doc_to_task()` serialization

---

## `.env.example`

```
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

Students copy this to `.env` and fill in their own credentials. The `.env` file must never be committed.

---

## Testing Checklist

```bash
# Unset the variable to test the startup error
unset MONGO_URI
python main.py
# Expected: clear error message, app exits

# Set the variable and run
export MONGO_URI="your_connection_string"
python main.py

# Full CRUD
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Persisted task"}'

curl http://localhost:5000/tasks

# Restart the server — data should still be there
```
