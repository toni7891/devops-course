from services.users_service import get_all_users
from services.posts_service import get_all_posts


def get_users_with_posts(limit=None):
    """
    Returns a list of users, each with their posts.

    Args:
        limit: maximum number of users to return (None = all)

    Returns:
        {"success": True, "data": [{name, email, posts}, ...]}
        {"success": False, "error": "..."}
    """
    users_result = get_all_users()
    if not users_result["success"]:
        return users_result

    posts_result = get_all_posts()
    if not posts_result["success"]:
        return posts_result

    users = users_result["data"]
    posts = posts_result["data"]

    if limit is not None:
        users = users[:limit]

    posts_by_user = {}
    for post in posts:
        posts_by_user.setdefault(post["userId"], []).append(post)

    result = [
        {
            "name": user["name"],
            "email": user["email"],
            "posts": posts_by_user.get(user["id"], [])
        }
        for user in users
    ]

    return {"success": True, "data": result}


# ── Bonus ─────────────────────────────────────────────────────────────────────

def get_top_users_by_posts(top_n=3):
    """
    BONUS: Returns the N users with the most posts.
    Sorted descending by post count.
    """
    result = get_users_with_posts()
    if not result["success"]:
        return result

    sorted_users = sorted(
        result["data"],
        key=lambda u: len(u["posts"]),
        reverse=True
    )

    top = sorted_users[:top_n]

    return {"success": True, "data": top}
