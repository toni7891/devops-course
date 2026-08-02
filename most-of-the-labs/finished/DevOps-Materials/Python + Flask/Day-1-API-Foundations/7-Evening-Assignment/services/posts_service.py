import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import time
from core.request_handler import make_request

BASE_URL = "https://jsonplaceholder.typicode.com"

_posts_cache = {}
MAX_RETRIES = 2


def get_all_posts(retries=MAX_RETRIES):
    """
    Fetch all posts with retry logic.
    Will try up to MAX_RETRIES times before giving up.
    """
    cache_key = "all_posts"

    if cache_key in _posts_cache:
        print("[CACHE] posts — returning from cache")
        return {"success": True, "data": _posts_cache[cache_key]}

    for attempt in range(1, retries + 1):
        print(f"[RETRY] posts — attempt {attempt}/{retries}")
        result = make_request(f"{BASE_URL}/posts")

        if result["success"]:
            _posts_cache[cache_key] = result["data"]
            return result

        if attempt < retries:
            time.sleep(1)

    return {"success": False, "error": f"Failed after {retries} attempts: {result.get('error')}"}


def get_posts_by_user(user_id, retries=MAX_RETRIES):
    """Fetch posts for a specific user with retry."""
    cache_key = f"posts_user_{user_id}"

    if cache_key in _posts_cache:
        print(f"[CACHE] posts for user {user_id} — returning from cache")
        return {"success": True, "data": _posts_cache[cache_key]}

    for attempt in range(1, retries + 1):
        result = make_request(
            f"{BASE_URL}/posts",
            params={"userId": user_id}
        )

        if result["success"]:
            _posts_cache[cache_key] = result["data"]
            return result

        if attempt < retries:
            time.sleep(1)

    return {"success": False, "error": f"Failed after {retries} attempts"}
