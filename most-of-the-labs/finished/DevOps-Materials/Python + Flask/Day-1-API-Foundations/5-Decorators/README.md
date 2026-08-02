# Decorators — Real Use Only

**Time:** 14:30–15:30

## The Problem

Every function that sends a request needs try/except → duplicated code.

```python
def fetch_users():
    try:
        ...
    except ...:
        return {"success": False, "error": "..."}

def fetch_posts():
    try:       # ← same logic again
        ...
    except ...:
        return {"success": False, "error": "..."}
```

**Why this is bad:**
- A single change needs to happen in dozens of places
- Easy to forget one exception type
- The function itself is unclear — logic buried in try

---

## The Solution — Decorator

```python
def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timed out"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    return wrapper
```

**Usage:**
```python
@handle_errors
def fetch_users():
    response = requests.get(url, timeout=5)   # clean!
    return {"success": True, "data": response.json()}
```

---

## How a Decorator Works

```python
@handle_errors
def fetch_users():
    ...

# equivalent to:
fetch_users = handle_errors(fetch_users)
```

`wrapper` wraps `fetch_users`:
1. Calls it
2. If it returned cleanly → return the result
3. If exception → return `{"success": False, ...}`

---

## log_execution decorator

```python
def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Starting: {func.__name__}")
        start = time.time()
        result = func(*args, **kwargs)
        print(f"[LOG] Done: {func.__name__} | {time.time()-start:.2f}s")
        return result
    return wrapper
```

**Order matters:**
```python
@log_execution    # registered first — runs first
@handle_errors    # registered second — runs second
def fetch_users():
    ...
```

---

## Exercise

See `decorators.py`

**Tasks:**
1. Understand `handle_errors` — what does it do?
2. Add a new exception: `ValueError`
3. Write a `@retry(times=2)` decorator that retries on failure
4. Wrap `fetch_users` with both and test it

**Bonus:** decorator with parameters:
```python
@retry(times=3)
def fetch_data():
    ...
```
