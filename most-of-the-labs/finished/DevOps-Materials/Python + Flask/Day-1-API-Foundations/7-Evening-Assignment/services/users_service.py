import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.request_handler import make_request

BASE_URL = "https://jsonplaceholder.typicode.com"

_users_cache = {}


def get_all_users():
    """
    Fetch all users with in-memory caching.
    Second call returns from cache, not from the API.
    """
    cache_key = "all_users"

    if cache_key in _users_cache:
        print("[CACHE] users — returning from cache")
        return {"success": True, "data": _users_cache[cache_key]}

    result = make_request(f"{BASE_URL}/users")

    if result["success"]:
        _users_cache[cache_key] = result["data"]

    return result


def get_user_by_id(user_id):
    """Fetch a single user by ID."""
    result = make_request(f"{BASE_URL}/users/{user_id}")
    return result
