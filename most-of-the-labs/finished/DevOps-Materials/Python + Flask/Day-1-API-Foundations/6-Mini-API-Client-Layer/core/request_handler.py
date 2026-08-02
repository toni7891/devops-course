import requests
from core.decorators import handle_errors, log_execution
from core.utils import build_response, check_status

BASE_URL = "https://jsonplaceholder.typicode.com"
DEFAULT_TIMEOUT = 5


@log_execution
@handle_errors
def make_request(url, method="GET", params=None, body=None):
    """
    Central function for sending HTTP requests.

    Args:
        url: full URL
        method: HTTP method (GET, POST, ...)
        params: query parameters as dict
        body: request body as dict (for POST/PUT)

    Returns:
        {"success": True, "data": ...}  or  {"success": False, "error": "..."}
    """
    response = requests.request(
        method=method.upper(),
        url=url,
        params=params,
        json=body,
        timeout=DEFAULT_TIMEOUT
    )

    status_error = check_status(response)
    if status_error:
        return status_error

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        return build_response(success=False, error="Response is not valid JSON")

    return build_response(success=True, data=data)


def get_users():
    return make_request(f"{BASE_URL}/users")


def get_posts(user_id=None):
    params = {"userId": user_id} if user_id else None
    return make_request(f"{BASE_URL}/posts", params=params)


def get_users_with_posts():
    """
    Fetches users and posts and joins them together.
    Uses make_request only — never requests directly.
    """
    users_result = get_users()
    if not users_result["success"]:
        return users_result

    posts_result = get_posts()
    if not posts_result["success"]:
        return posts_result

    users = users_result["data"]
    posts = posts_result["data"]

    posts_by_user = {}
    for post in posts:
        posts_by_user.setdefault(post["userId"], []).append(post)

    result = [
        {
            "name": user["name"],
            "posts": posts_by_user.get(user["id"], [])
        }
        for user in users
    ]

    return build_response(success=True, data=result)
