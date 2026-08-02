from core.request_handler import get_users, get_posts, get_users_with_posts


def main():
    print("=" * 50)
    print("Mini API Client Layer — Demo")
    print("=" * 50)

    print("\n--- get_users() ---")
    result = get_users()
    if result["success"]:
        print(f"Got {len(result['data'])} users")
        for u in result["data"][:3]:
            print(f"  · {u['name']}")
    else:
        print(f"Error: {result['error']}")

    print("\n--- get_posts(user_id=1) ---")
    result = get_posts(user_id=1)
    if result["success"]:
        print(f"Got {len(result['data'])} posts for user 1")
    else:
        print(f"Error: {result['error']}")

    print("\n--- get_users_with_posts() ---")
    result = get_users_with_posts()
    if result["success"]:
        for entry in result["data"][:3]:
            print(f"  · {entry['name']}: {len(entry['posts'])} posts")
    else:
        print(f"Error: {result['error']}")


if __name__ == "__main__":
    main()
