# Working with `requests`

**Time:** 11:00–12:15

## Topics

### Installation
```bash
pip install requests
```

### requests.get()
```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")
```

### status_code
```python
print(response.status_code)  # 200
```

### response.json()
```python
data = response.json()  # returns dict / list
print(type(data))       # <class 'list'>
```

### params
```python
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1}
)
# sends: GET /posts?userId=1
```

---

## Guided Exercise

**Build `fetch_users()` with the class — see `fetch_users.py`**

Step by step:
1. `import requests`
2. `response = requests.get(...)`
3. `print(response.status_code)`
4. `users = response.json()`
5. `return users`

---

## Independent Exercise — "User-Post Mapper"

**Goal:** Build `get_users_with_posts()` on their own.

**APIs:**
- `GET /users` → all users
- `GET /posts` → all posts (each post has a `userId` field)

**Required output format:**
```python
[
    {
        "name": "Leanne Graham",
        "posts": [
            {"id": 1, "title": "..."},
            ...
        ]
    }
]
```

**Where they'll get stuck (and that's fine!):**
- How to connect users to posts?
- A dict with `userId` as the key — this is the insight they need to reach

**After they get stuck** — show the solution in `fetch_users.py` and explain the grouping pattern.

---

## 12:15–12:30 — Debrief

Ask the class:
- What was the hardest part?
- Why is it wrong to mix logic together?
- What happens if the API fails?

This is the bridge to the next section — Error Handling.
