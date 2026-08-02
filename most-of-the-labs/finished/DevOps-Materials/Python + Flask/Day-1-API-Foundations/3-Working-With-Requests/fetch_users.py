import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ── Guided Exercise ───────────────────────────────────────────────────────────

def fetch_users():
    """Fetch the list of all users from the API."""
    response = requests.get(f"{BASE_URL}/users")
    print(f"Status Code: {response.status_code}")
    users = response.json()
    print(f"Number of users: {len(users)}")
    return users


def fetch_posts():
    """Fetch all posts from the API."""
    response = requests.get(f"{BASE_URL}/posts")
    return response.json()


def fetch_posts_by_user(user_id):
    """Fetch posts for a specific user using params."""
    response = requests.get(
        f"{BASE_URL}/posts",
        params={"userId": user_id}
    )
    return response.json()


# ── Independent Exercise: User-Post Mapper ────────────────────────────────────

def get_users_with_posts():
    """
    Returns a list of users, each with their posts.

    Return format:
    [
        {
            "name": "Leanne Graham",
            "posts": [
                {"id": 1, "title": "..."},
                ...
            ]
        },
        ...
    ]
    """
    users = fetch_users()
    posts = fetch_posts()

    # TODO: build the mapping
    # Hint: build a dict of user_id -> posts first
    result = []

    posts_by_user = {}
    for post in posts:
        uid = post["userId"]
        if uid not in posts_by_user:
            posts_by_user[uid] = []
        posts_by_user[uid].append(post)

    for user in users:
        result.append({
            "name": user["name"],
            "posts": posts_by_user.get(user["id"], [])
        })

    return result


if __name__ == "__main__":
    print("=== Fetching Users ===")
    users = fetch_users()
    for u in users[:3]:
        print(f"  - {u['name']} ({u['email']})")

    print("\n=== User-Post Mapper ===")
    mapped = get_users_with_posts()
    for entry in mapped[:2]:
        print(f"\n{entry['name']}: {len(entry['posts'])} posts")
        for post in entry["posts"][:2]:
            print(f"  -> {post['title'][:50]}...")
