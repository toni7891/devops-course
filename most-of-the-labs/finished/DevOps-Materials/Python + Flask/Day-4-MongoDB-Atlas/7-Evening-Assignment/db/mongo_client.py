import os
import time

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

load_dotenv()

MAX_RETRIES = 2
_client: MongoClient | None = None


def _get_uri() -> str:
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise RuntimeError(
            "MONGO_URI environment variable is not set. "
            "Copy .env.example to .env and fill in your credentials."
        )
    return uri


def init_db() -> None:
    """Connect to MongoDB Atlas with retry logic. Call once at startup."""
    global _client
    uri = _get_uri()
    last_error = None

    for attempt in range(1, MAX_RETRIES + 2):
        try:
            print(f"[DB] Connecting to MongoDB Atlas (attempt {attempt})...")
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")
            _client = client
            print("[DB] Connected to MongoDB Atlas.")
            return
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            last_error = e
            print(f"[DB] Attempt {attempt} failed: {e}")
            if attempt <= MAX_RETRIES:
                print(f"[DB] Retrying in 1 second...")
                time.sleep(1)

    raise RuntimeError(
        f"Could not connect to MongoDB Atlas after {MAX_RETRIES + 1} attempts. "
        f"Last error: {last_error}"
    )


def get_collection(name: str) -> Collection:
    if _client is None:
        raise RuntimeError("Database not initialised. Call init_db() first.")
    return _client["task_manager"][name]
