import functools
import time
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ── The Problem — duplicated code ─────────────────────────────────────────────

def fetch_users_bad():
    """Every function must duplicate the try/except — this is bad."""
    try:
        response = requests.get(f"{BASE_URL}/users", timeout=5)
        if response.status_code != 200:
            return {"success": False, "error": f"Status {response.status_code}"}
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def fetch_posts_bad():
    """Exact same logic — again and again."""
    try:
        response = requests.get(f"{BASE_URL}/posts", timeout=5)
        if response.status_code != 200:
            return {"success": False, "error": f"Status {response.status_code}"}
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# ── The Solution — Decorators ─────────────────────────────────────────────────

def handle_errors(func):
    """
    Decorator that wraps any function with unified error handling.
    The wrapped function should return a dict with "data" or raise an exception.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Could not connect to server"}
        except requests.exceptions.JSONDecodeError:
            return {"success": False, "error": "Invalid JSON response"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
    return wrapper


def log_execution(func):
    """
    Decorator that prints before and after execution, including elapsed time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Starting: {func.__name__}")
        start = time.time()

        result = func(*args, **kwargs)

        elapsed = time.time() - start
        status = "OK" if isinstance(result, dict) and result.get("success") else "FAILED"
        print(f"[LOG] Done: {func.__name__} | status={status} | time={elapsed:.2f}s")

        return result
    return wrapper


# ── Actual Usage ──────────────────────────────────────────────────────────────

@log_execution
@handle_errors
def fetch_users():
    """Now the function itself is clean — just the logic."""
    response = requests.get(f"{BASE_URL}/users", timeout=5)
    if response.status_code != 200:
        return {"success": False, "error": f"Status {response.status_code}"}
    return {"success": True, "data": response.json()}


@log_execution
@handle_errors
def fetch_posts():
    response = requests.get(f"{BASE_URL}/posts", timeout=5)
    if response.status_code != 200:
        return {"success": False, "error": f"Status {response.status_code}"}
    return {"success": True, "data": response.json()}


@log_execution
@handle_errors
def fetch_data_from_bad_url():
    """Simulate a failure."""
    response = requests.get("https://not-a-real-url.xyz/data", timeout=3)
    return {"success": True, "data": response.json()}


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== fetch_users ===")
    result = fetch_users()
    if result["success"]:
        print(f"  Got {len(result['data'])} users\n")

    print("=== fetch_posts ===")
    result = fetch_posts()
    if result["success"]:
        print(f"  Got {len(result['data'])} posts\n")

    print("=== bad URL (expected failure) ===")
    result = fetch_data_from_bad_url()
    print(f"  success={result['success']}, error={result.get('error')}\n")
