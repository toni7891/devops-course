from services.aggregator_service import get_users_with_posts, get_top_users_by_posts


def main():
    print("=" * 55)
    print("External API Integration Layer v1")
    print("=" * 55)

    print("\n--- get_users_with_posts() — כל המשתמשים ---")
    result = get_users_with_posts()
    if result["success"]:
        for entry in result["data"][:3]:
            print(f"  {entry['name']}: {len(entry['posts'])} posts")
    else:
        print(f"Error: {result['error']}")

    print("\n--- get_users_with_posts(limit=3) ---")
    result = get_users_with_posts(limit=3)
    if result["success"]:
        print(f"  Got {len(result['data'])} users (limited)")
        for entry in result["data"]:
            print(f"  {entry['name']}: {len(entry['posts'])} posts")

    print("\n--- CACHE TEST: קריאה שנייה (אמורה להגיע מcache) ---")
    result = get_users_with_posts(limit=2)
    if result["success"]:
        print(f"  Got {len(result['data'])} users")

    print("\n--- BONUS: get_top_users_by_posts(top_n=3) ---")
    result = get_top_users_by_posts(top_n=3)
    if result["success"]:
        print("  Top 3 users by post count:")
        for i, entry in enumerate(result["data"], 1):
            print(f"  {i}. {entry['name']}: {len(entry['posts'])} posts")
    else:
        print(f"Error: {result['error']}")


if __name__ == "__main__":
    main()
