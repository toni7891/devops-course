# Evening Assignment — External API Integration Layer v1

## Structure

```
7-Evening-Assignment/
├── core/
│   ├── request_handler.py   ← make_request (copied from exercise 6)
│   ├── decorators.py
│   └── utils.py
├── services/
│   ├── users_service.py     ← get_all_users() with caching
│   ├── posts_service.py     ← get_all_posts() with retry
│   └── aggregator_service.py← get_users_with_posts() + bonus
└── main.py
```

---

## Run

```bash
cd 7-Evening-Assignment
python main.py
```

---

## Requirements

### Iron Rule
- **Every** API call goes through `make_request`
- **Forbidden** to import `requests` directly in services

### Required Functions

| Function | File | Features |
|----------|------|---------|
| `get_all_users()` | users_service | in-memory caching |
| `get_all_posts()` | posts_service | retry x2, caching |
| `get_users_with_posts(limit)` | aggregator_service | limit, unified structure |

### Advanced Features (required)

**Caching:**
```python
_cache = {}

def get_all_users():
    if "users" in _cache:
        return {"success": True, "data": _cache["users"]}
    result = make_request(...)
    if result["success"]:
        _cache["users"] = result["data"]
    return result
```

**Retry:**
```python
for attempt in range(1, MAX_RETRIES + 1):
    result = make_request(...)
    if result["success"]:
        return result
    time.sleep(1)
return {"success": False, "error": "Failed after retries"}
```

**Limit:**
```python
def get_users_with_posts(limit=None):
    ...
    if limit:
        users = users[:limit]
```

### Bonus (for strong students)

```python
def get_top_users_by_posts(top_n=3):
    # sort by len(posts) descending
    # return only top_n
```

---

## Expected Output

```
[LOG] → make_request()
[LOG] ← make_request() | OK | 0.412s
[CACHE] users — returning from cache
[LOG] → make_request()
[LOG] ← make_request() | OK | 0.389s
[CACHE] posts — returning from cache

Top 3 users by post count:
1. Ervin Howell: 10 posts
2. Leanne Graham: 10 posts
3. Clementine Bauch: 10 posts
```
