# Final Exercise — Mini API Client Layer

**Time:** 15:30–16:30

## Structure

```
6-Mini-API-Client-Layer/
├── core/
│   ├── request_handler.py   ← the heart: make_request + specific functions
│   ├── decorators.py        ← handle_errors + log_execution
│   └── utils.py             ← build_response + check_status
└── main.py                  ← actual usage
```

---

## Run

```bash
cd 6-Mini-API-Client-Layer
python main.py
```

---

## Requirements (for students)

### 1. Central function in `core/request_handler.py`

```python
make_request(url, method="GET", params=None)
```

**Must:**
- Handle timeout
- Handle status != 200
- Handle JSON decode errors
- Always return a unified structure

---

### 2. Decorators in `core/decorators.py`

```python
@handle_errors
@log_execution
```

- `handle_errors` — all exceptions
- `log_execution` — function name + elapsed time + result

---

### 3. Unified response structure always

```json
{"success": true, "data": [...]}
{"success": false, "error": "..."}
```

---

### 4. Working function

```python
get_users_with_posts()
```

**Must** use `make_request` only.
**Must not** use `requests` directly.

---

## Key Points to Emphasize

- Decorator order: `@log_execution` above `@handle_errors` — why?
  - log sees what handle_errors returns (including errors)
- `functools.wraps` — preserves the original function name
- `build_response` — everyone returns the same format
- `check_status` — DRY principle
