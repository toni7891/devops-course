# FastAPI Lab: Speed with Type Safety — A Beginner's Journey

> **You know Flask. Now let's meet FastAPI.**
>
> Flask gives you freedom. Django gives you batteries.
> FastAPI gives you **speed** and **automatic documentation**.

---

## The Story: The Race Car vs The Family Car

Imagine choosing a car:

**Flask is like a classic car:**
- Simple, reliable, you know how everything works
- You build features yourself
- Good for Sunday drives

**Django is like a family SUV:**
- Comes with everything built-in (GPS, safety features, spacious)
- Follows the rules, gets you there safely
- Great for road trips with the family

**FastAPI is like a race car:**
- Built for speed (async engine)
- Automatic systems monitor everything (type checking)
- Built-in dashboard shows all stats (auto docs)

---

## Chapter 1: What Makes FastAPI Different?

### The Problem You Face

In Flask, you write a lot of validation code:

```python
# Flask style (what you know)
from flask import request, jsonify

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    
    # Manual validation - lots of code!
    if not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
    if len(data['name']) < 2:
        return jsonify({"error": "Name too short"}), 400
    if '@' not in data.get('email', ''):
        return jsonify({"error": "Invalid email"}), 400
    
    # Finally create the student...
```

**This works, but:**
- Lots of boilerplate validation code
- You write the same checks over and over
- No automatic API documentation
- Manual type conversion (string "42" → int 42)

### The FastAPI Solution: Type Hints

**FastAPI uses Python type hints to do everything automatically:**

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str
    role: str = Field(default="student", pattern="^(student|teacher|admin)$")

@app.post("/students")
async def create_student(student: StudentCreate):
    # FastAPI already validated everything!
    # If validation fails, it returns 422 with detailed errors automatically
    return {"id": 1, **student.model_dump()}
```

**What FastAPI does for you:**

| What You Used to Do | What FastAPI Does |
|---------------------|-------------------|
| Check if field exists | Automatic - fields are required by default |
| Validate string length | `Field(min_length=2)` handles it |
| Validate email format | `EmailStr` type handles it |
| Validate against choices | `pattern="^(student|teacher\|admin)$"` handles it |
| Return error responses | Automatic 422 with detailed field errors |
| Create API documentation | Auto-generated at `/docs` |

---

## Setup (Do This First)

### Python Version

**This lab requires Python 3.14**

Check your version:
```bash
python3 --version
# Should show: Python 3.14.x
```

If you have a different version, install Python 3.14 from python.org

**Note:** Python 3.14 requires a compatibility flag for Pydantic (used by FastAPI). The commands below include this workaround.

### Windows Users

**Option 1: Use Git Bash (Recommended)**
- Git Bash provides the same commands as macOS/Linux
- All commands below work exactly as written

**Option 2: Use Command Prompt/PowerShell**
Replace `python3` with `python` and `source venv/bin/activate` with `venv\Scripts\activate`:
```cmd
cd Python\fastapi_app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Setup Commands (macOS/Linux/Git Bash)

```bash
# 1. Navigate to FastAPI project
cd Python/fastapi_app

# 2. Create virtual environment (first time only)
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
# For Python 3.14 (newer versions), use this workaround:
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 pip install -r requirements.txt

# For Python 3.10-3.13, just use:
# pip install -r requirements.txt

# 5. Run the server
uvicorn main:app --reload

# Server starts at http://localhost:8000
```


**What is uvicorn?**
Think of it like this:
- **Your Python code** = The restaurant kitchen (cooks the food)
- **Uvicorn** = The waiter (takes orders from customers, brings them to kitchen, delivers food back)
- It handles multiple customers at once using **async** (ASGI)

**What's the difference between WSGI and ASGI?**

| | WSGI (Flask/Django classic) | ASGI (FastAPI) |
|---|---|---|
| **Analogy** | One cashier, one order at a time | Multiple self-checkout machines |
| **How it works** | Each request blocks until done | Requests can "pause" and let others run |
| **Best for** | Simple apps | High-traffic APIs |

Think of WSGI like a bank with one teller - customers wait in line. ASGI is like a bank with many ATMs - customers work in parallel.

---

## Chapter 2: The Magic of Automatic Docs

### What is Swagger/OpenAPI?

**Swagger UI** = An interactive webpage that shows your API:
- Lists all your endpoints (URLs)
- Shows what parameters each endpoint needs
- Lets you test endpoints directly in the browser
- Updates automatically when you change your code

**Analogy:** It's like a restaurant menu that:
- Shows all dishes (endpoints)
- Lists ingredients (parameters)
- Lets you place orders (test API)
- Updates itself when the chef changes recipes

**Why it's useful:**
- Frontend developers can see exactly how to call your API
- You can test without writing any code
- Documentation never gets out of date (it's generated from code)

---

### Try It Now

**Try it now:**

1. Visit: http://localhost:8000/docs
2. You see Swagger UI with all your endpoints!
3. Click on any endpoint → See parameters, request body, responses
4. Click "Try it out" → Test the API directly in the browser!

**How it works:**
```
Your Type Hints (code)
         ↓
FastAPI reads your function signature
         ↓
Generates OpenAPI schema
         ↓
/docs shows interactive Swagger UI
```

### Exercise: Explore the Auto-Docs

1. Visit http://localhost:8000/docs
2. Find the `POST /students` endpoint
3. Click "Try it out"
4. Enter this JSON:
   ```json
   {
     "name": "Charlie",
     "email": "charlie@example.com",
     "role": "student"
   }
   ```
5. Click "Execute"

**Result:** You made an API call and can see the exact request/response!

---

## Chapter 3: Type Hints = Validation

### The Pydantic Magic

FastAPI uses **Pydantic** for data validation. Think of it as a strict bouncer at a club:

```python
from pydantic import BaseModel, Field, EmailStr

class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr  # Must be valid email format
    role: str = Field(default="student", pattern="^(student|teacher|admin)$")
```

### Exercise: Test Automatic Validation

Try sending bad data via the `/docs` interface:

**Test 1: Name too short**
```json
{
  "name": "A",
  "email": "test@example.com",
  "role": "student"
}
```
**Result:** 422 error - "name: String should have at least 2 characters"

**Test 2: Invalid email**
```json
{
  "name": "Alice",
  "email": "not-an-email",
  "role": "student"
}
```
**Result:** 422 error - "email: value is not a valid email address"

**Test 3: Invalid role**
```json
{
  "name": "Alice",
  "email": "alice@example.com",
  "role": "hacker"
}
```
**Result:** 422 error - "role: String should match pattern..."

**Compare to Flask:** In Flask, you'd write all these checks manually. FastAPI does it automatically from type hints!

---

## Chapter 4: Dependency Injection — The Secret Weapon

### What is Dependency Injection?

**The Problem:** Without dependency injection, you repeat code in every endpoint:

```python
# ❌ WITHOUT Depends - Code repeated in every endpoint:
@app.get("/students")
async def list_students():
    db = connect_to_database()  # Repeated
    result = db.query("SELECT * FROM students")
    db.close()                  # Repeated
    return result

@app.post("/students")
async def create_student(student: StudentCreate):
    db = connect_to_database()  # Repeated again!
    db.insert(student)
    db.close()                  # Repeated again!
    return student

# Imagine 20 more endpoints... all repeating the same db code!
```

**The Solution:** FastAPI **injects** dependencies automatically:

```python
# ✅ WITH Depends - Write once, use everywhere:
from fastapi import Depends

def get_db():           # Define dependency once
    db = connect_to_database()
    yield db            # FastAPI handles cleanup after request
    db.close()

@app.get("/students")   # Use in any endpoint
async def list_students(db = Depends(get_db)):
    return db.query("SELECT * FROM students")
    # No cleanup needed - FastAPI does it!

@app.post("/students")  # Same dependency, zero repetition
async def create_student(student: StudentCreate, db = Depends(get_db)):
    return db.insert(student)
```

**Analogy: Making Coffee**

| Without Depends | With Depends |
|-----------------|--------------|
| Every morning: grind beans, boil water, brew, clean up | Put cup under the machine, coffee appears |
| You do all the work every time | Someone else (FastAPI) handles the setup/cleanup |
| Messy and repetitive | Clean and simple |

**What FastAPI does for you:**
1. **Calls** `get_db()` before your function runs
2. **Passes** the result as the `db` parameter
3. **Cleans up** after your function finishes (if you use `yield`)

**Benefits:**
- **Less code** - Write database logic once, use in 20 endpoints
- **Automatic cleanup** - No more forgetting to close connections
- **Easy testing** - Replace `get_db` with a fake database for tests

### Exercise: Add a Simple Auth Dependency

**What is a Bearer Token?**

Think of it like a **concert wristband**:
1. You buy a ticket (login) → Get a wristband (token)
2. Show wristband at the gate (API endpoint) → They let you in
3. No wristband? → "Sorry, you can't enter" (401 error)

**Bearer** means "whoever carries this token" - like cash, whoever holds it can use it.

**Where does the token come from?**

In this exercise, we use a **hardcoded token** for simplicity:
- Token value: `secret-token` (set in the code)
- You send: `Bearer secret-token` in the Authorization header
- The code checks: `if credentials.credentials != "secret-token":` → reject if wrong

In real apps, tokens come from a login endpoint that validates username/password and returns a JWT token.

---

**Open `main.py` and find the commented section:**

```python
# UNCOMMENT FOR AUTH EXERCISE:
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#
# security = HTTPBearer()
#
# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     """Simple token auth - in production, validate JWT"""
#     if credentials.credentials != "secret-token":
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return {"username": "testuser"}
```

**Step 1:** Uncomment the auth dependency code (remove the `#` at start of lines)

**Step 2:** Find the protected endpoint and uncomment:

```python
# UNCOMMENT FOR AUTH EXERCISE (add to endpoint):
# async def get_protected_data(user: dict = Depends(get_current_user)):
#     return {"message": f"Hello {user['username']}, you accessed protected data!"}
```

**Step 3:** Add the route (find commented section):

```python
# UNCOMMENT FOR AUTH EXERCISE (add route):
# @app.get("/protected", tags=["Auth"])
# async def protected_endpoint(user: dict = Depends(get_current_user)):
#     return {"message": f"Hello {user['username']}, you accessed protected data!"}
```

**Step 4:** Restart the server (`Ctrl+C`, then `uvicorn main:app --reload`)

**Step 5:** Test in `/docs`:
1. Visit http://localhost:8000/docs
2. Find `/protected` endpoint
3. Click "Authorize" button (top right)
4. Enter: `Bearer secret-token`
5. Now you can call `/protected`!

**Try without token:** 401 Unauthorized error!

---

## Chapter 5: Async — Why It Matters

### Sync vs Async

**Sync (Flask/Django classic):**
```
Request 1 arrives → Process → Wait for DB → Response
Request 2 arrives → WAIT → Process → Wait for DB → Response
```
One request blocks the thread.

**Async (FastAPI):**
```
Request 1 arrives → Process → WAIT FOR DB (yield control)
Request 2 arrives → Process immediately!
Request 1 DB returns → Resume Request 1 → Response
```
One worker handles thousands of requests.

### Exercise: Test Async Performance

FastAPI app has an async demo endpoint with a **5 second delay** (for easy testing). Test it:

**You need TWO terminal windows open:**

**Terminal 1:**
```bash
curl http://localhost:8000/async-demo
# This takes 5 seconds
```

**Terminal 2 (immediately after Terminal 1):**
```bash
curl http://localhost:8000/
# This responds instantly!
```

**Result:** Terminal 2 finishes immediately (200 OK) while Terminal 1 is still waiting! That's async in action.

**In a sync framework (Flask),** Terminal 2 would wait for Terminal 1 to finish (5+ seconds).

**The code behind it:**
```python
@app.get("/async-demo")
async def async_demo():
    await asyncio.sleep(5)  # Non-blocking sleep!
    return {"message": "Done"}
```

`await` tells Python: "I'm waiting, go handle other requests."

---

## Chapter 6: Testing the API with curl

```bash
# Get all students
curl http://localhost:8000/students

# Create a student
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie", "email": "charlie@example.com", "role": "student"}'

# Get one student
curl http://localhost:8000/students/1

# Update a student (PATCH - partial update)
curl -X PATCH http://localhost:8000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"role": "teacher"}'

# Delete a student
curl -X DELETE http://localhost:8000/students/1

# Filter with query params
curl "http://localhost:8000/students?role=student&is_active=true"
```

---

## Quick Reference: FastAPI Cheat Sheet

| What You Want | How to Do It |
|---------------|--------------|
| Create endpoint | `@app.get("/path")`, `@app.post("/path")`, etc. |
| Path parameter | `student_id: int` in function args |
| Query parameter | `role: Optional[str] = Query(None)` |
| Request body | `student: StudentCreate` (Pydantic model) |
| Response model | `response_model=StudentResponse` decorator arg |
| Dependency | `db: dict = Depends(get_db)` |
| Raise HTTP error | `raise HTTPException(status_code=404, detail="Not found")` |
| Auto docs | Visit `/docs` (Swagger) or `/redoc` (ReDoc) |

---

## Chapter 7: Testing Your API

### Run the Included Tests

A test file `test_main.py` is included. Run it:

```bash
# Install test dependencies (already in requirements.txt)
pip install pytest httpx

# Run all tests
pytest test_main.py -v

# Run specific test
pytest test_main.py::test_create_student_success -v
```

### What the Tests Cover

- ✅ Root endpoint returns app info
- ✅ GET /students returns list
- ✅ POST /students creates with valid data
- ✅ POST /students rejects invalid data (422)
- ✅ GET /students/{id} returns single student
- ✅ GET /students/{id} returns 404 for invalid ID

### Learn More

See `../LAB_Testing.md` for comprehensive testing guide covering:
- pytest fundamentals
- Fixtures and mocking
- Testing Flask and Django apps
- Async testing

---

## Summary: Flask vs Django vs FastAPI

| Feature | Flask | Django | FastAPI |
|---------|-------|--------|---------|
| **Philosophy** | "Do it yourself" | "Batteries included" | "Fast & type-safe" |
| **Speed** | Medium | Medium | **Very Fast** (async) |
| **Validation** | Manual | Forms/DRF | **Automatic** (type hints) |
| **Auto docs** | No | No (third-party) | **Yes** (built-in) |
| **Async** | Limited | Partial | **Native** |
| **Learning** | Easy | Steep | Medium |
| **Best for** | Small apps, learning | Full web apps | **High-performance APIs** |

**Remember:**
- Use **Flask** when you want control and simplicity
- Use **Django** when you need a full admin, ORM, and convention
- Use **FastAPI** when you need speed, auto docs, and type safety

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named fastapi" | Activate venv: `source venv/bin/activate` |
| Port already in use | `lsof -ti:8000 \| xargs kill -9` then restart |
| Changes not showing | Check `--reload` flag is set |
| Validation errors not clear | Check `/docs` for exact schema |
| **Pydantic build error on Python 3.14** | Upgrade requirements: `pip install fastapi==0.115.12 uvicorn==0.34.2 pydantic==2.11.3` |

**Note:** Python 3.14 is very new. If you get build errors with Pydantic, make sure you have the latest versions in `requirements.txt`. Pydantic uses Rust internally and needs updates for new Python versions.

---

## Next Steps

1. **Explore the code:** Look at `main.py` - every line is documented
2. **Add a field:** Edit `StudentCreate` model, reload `/docs`
3. **Add a new endpoint:** Copy an existing route pattern
4. **Try SQLAlchemy:** Replace in-memory DB with real database
