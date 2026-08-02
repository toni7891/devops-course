import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ── Version 1: no error handling (show what happens when something breaks) ────

def fetch_users_naive():
    """Naive version — crashes if anything fails."""
    response = requests.get(f"{BASE_URL}/users")
    return response.json()


# ── Version 2: with error handling ───────────────────────────────────────────

def fetch_users_safe():
    """Safe version — always returns a unified structure."""
    try:
        response = requests.get(f"{BASE_URL}/users", timeout=5)

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API returned status {response.status_code}"
            }

        return {
            "success": True,
            "data": response.json()
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Could not connect to server"
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out"
        }

    except requests.exceptions.JSONDecodeError:
        return {
            "success": False,
            "error": "Response was not valid JSON"
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }


# ── Exercise: wrap the mapper ─────────────────────────────────────────────────

def get_users_with_posts_safe():
    """
    Safe version of the User-Post Mapper from the previous section.

    Requirements:
    - On failure -> does not crash
    - Returns {"success": False, "error": "..."}
    - On success -> {"success": True, "data": [...]}
    """
    try:
        users_resp = requests.get(f"{BASE_URL}/users", timeout=5)
        posts_resp = requests.get(f"{BASE_URL}/posts", timeout=5)

        if users_resp.status_code != 200:
            return {"success": False, "error": f"Users API failed: {users_resp.status_code}"}

        if posts_resp.status_code != 200:
            return {"success": False, "error": f"Posts API failed: {posts_resp.status_code}"}

        users = users_resp.json()
        posts = posts_resp.json()

        posts_by_user = {}
        for post in posts:
            uid = post["userId"]
            posts_by_user.setdefault(uid, []).append(post)

        result = [
            {"name": user["name"], "posts": posts_by_user.get(user["id"], [])}
            for user in users
        ]

        return {"success": True, "data": result}

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Safe fetch ===")
    result = fetch_users_safe()
    if result["success"]:
        print(f"Got {len(result['data'])} users")
    else:
        print(f"Error: {result['error']}")

    print("\n=== Safe mapper ===")
    result = get_users_with_posts_safe()
    if result["success"]:
        for entry in result["data"][:2]:
            print(f"{entry['name']}: {len(entry['posts'])} posts")
    else:
        print(f"Error: {result['error']}")