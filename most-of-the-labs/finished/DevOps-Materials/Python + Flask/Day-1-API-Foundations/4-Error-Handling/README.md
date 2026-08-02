# Error Handling — Not Theory, Practice

**Time:** 13:30–14:30

## Why It Matters

Networks fail. Servers return 500. JSON is malformed.
Code without error handling = code that crashes in production.

---

## The Three Possible Failures

### 1. Network failure
```python
requests.exceptions.ConnectionError
requests.exceptions.Timeout
```

### 2. Server returned an error
```python
response.status_code != 200
# 404, 500, 403, ...
```

### 3. Invalid JSON
```python
requests.exceptions.JSONDecodeError
response.json()  # raises if body is not JSON
```

---

## Basic try/except Structure

```python
try:
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        return {"success": False, "error": f"Status {response.status_code}"}

    return {"success": True, "data": response.json()}

except requests.exceptions.Timeout:
    return {"success": False, "error": "Request timed out"}

except requests.exceptions.ConnectionError:
    return {"success": False, "error": "Could not connect"}

except requests.exceptions.RequestException as e:
    return {"success": False, "error": str(e)}
```

---

## Unified Response Structure

```json
{"success": true, "data": [...]}
```

```json
{"success": false, "error": "Request timed out"}
```

**Why a unified structure?**
- The calling code doesn't need to know what went wrong
- Easy to check: `if result["success"]:`
- Consistent throughout the entire codebase

---

## Exercise — Wrap the Mapper

See `error_handling.py`

**Requirements:**
1. Wrap `get_users_with_posts` in try/except
2. On failure — don't crash, return `{"success": False, "error": "..."}`
3. Handle separately: ConnectionError, Timeout, status != 200
4. Test: what happens with a bad URL?

**To simulate failures:**
```python
# Bad URL
requests.get("https://not-a-real-url.xyz/users", timeout=3)

# Status != 200
requests.get("https://jsonplaceholder.typicode.com/users/9999")
```
