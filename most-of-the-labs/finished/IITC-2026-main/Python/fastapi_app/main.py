"""
=============================================================================
FASTAPI — Modern, Fast, Async Web Framework
=============================================================================

WHAT IS FASTAPI?
FastAPI is a modern Python web framework built on two key libraries:
  - Starlette: the ASGI framework handling routing, middleware, and requests
  - Pydantic: data validation and serialization using Python type hints

HOW IT WORKS BEHIND THE SCENES:

1. ASGI (Async Server Gateway Interface)
   Unlike WSGI (Flask/Django), ASGI is non-blocking.
   When your handler does `await some_db_query()`, the event loop
   suspends this coroutine and serves other requests during the wait.
   One uvicorn worker can handle thousands of concurrent connections.

   WSGI model:      1 request = 1 thread (blocked during I/O)
   ASGI model:      1 event loop = many requests (suspended during I/O)

2. TYPE HINTS → AUTOMATIC VALIDATION & DOCS
   FastAPI inspects function signatures using Python's `inspect` module
   and `typing`. When it sees `def get_user(user_id: int)`, it:
     a) Automatically converts the URL string "42" to Python int 42
     b) Returns 422 Unprocessable Entity if conversion fails
     c) Documents this parameter in the OpenAPI schema

   When it sees a Pydantic model as a parameter:
     a) Parses the JSON request body
     b) Validates each field (type, constraints, required/optional)
     c) Returns detailed validation errors if invalid
     d) Adds the full schema to the OpenAPI docs

3. AUTOMATIC API DOCUMENTATION
   FastAPI builds an OpenAPI 3.0 schema at startup by introspecting all
   routes, their parameters, request bodies, and response models.
   - Swagger UI at /docs — interactive, you can make requests from the browser
   - ReDoc at /redoc — cleaner read-only documentation
   This replaces hours of manual documentation writing.

4. DEPENDENCY INJECTION
   FastAPI has a built-in DI system. `Depends(get_db)` tells FastAPI to
   call `get_db()` first and pass its result to your handler. Great for:
   - Database sessions (create on request start, close on end)
   - Authentication (extract and verify token, pass user to handler)
   - Configuration and shared state

WHEN TO USE FASTAPI:
  - REST APIs that need to be fast and handle high concurrency
  - When auto-generated OpenAPI docs are valuable (public APIs, team work)
  - Type-safety is important to you
  - Modern Python (3.10+) projects

WHEN NOT TO USE FASTAPI:
  - You need a full admin panel → use Django
  - Rendering server-side HTML → Django/Flask are more mature
  - The team is not comfortable with async Python → stick with Flask
=============================================================================
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import asyncio
from datetime import datetime

# ---------------------------------------------------------------------------
# 1. The Application Object
# ---------------------------------------------------------------------------
# FastAPI() creates the ASGI application.
# The metadata below populates your /docs page automatically.

app = FastAPI(
    title="FastAPI Educational App",
    description=(
        "A teaching example showing how FastAPI works: type hints for validation, "
        "Pydantic for schemas, async handlers, dependency injection, and auto docs."
    ),
    version="1.0.0",
    # Change the default docs URL if needed:
    # docs_url="/api/docs", redoc_url="/api/redoc"
)


# ---------------------------------------------------------------------------
# 2. Pydantic Models — The Heart of FastAPI's Type Safety
# ---------------------------------------------------------------------------
# Pydantic models define the shape of data. FastAPI uses them for:
#   - Request body validation and parsing
#   - Response serialization and filtering
#   - OpenAPI schema generation
#
# BEHIND THE SCENES:
# Pydantic v2 uses Rust under the hood (pydantic-core) for extremely fast
# validation. When you annotate a field with `str`, Pydantic will coerce
# compatible types (e.g. int → str) or raise a ValidationError.

class StudentCreate(BaseModel):
    """
    Schema for creating a student (request body).
    FastAPI will read the JSON body, validate against this, and give you
    a clean Python object — or return a 422 with detailed errors.
    """
    name: str = Field(
        ...,                    # ... means required (no default)
        min_length=2,
        max_length=100,
        description="Student's full name",
        examples=["Alice Smith"]
    )
    email: EmailStr = Field(
        ...,
        description="Student's email address (must be valid format)",
        examples=["alice@example.com"]
    )
    role: str = Field(
        default="student",
        pattern="^(student|teacher|admin)$",  # Regex validation
        description="Role must be: student, teacher, or admin"
    )


class StudentUpdate(BaseModel):
    """
    Schema for partial updates (PATCH). All fields are Optional.
    Pydantic lets you send only the fields you want to change.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[str] = Field(None, pattern="^(student|teacher|admin)$")
    is_active: Optional[bool] = None


class StudentResponse(BaseModel):
    """
    Schema for responses. FastAPI filters the output through this model —
    any fields not listed here are EXCLUDED from the response,
    which is a security feature (prevents accidentally leaking internal fields).
    """
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        # Allow creating this model from ORM objects (orm_mode in Pydantic v1)
        # In Pydantic v2, it's `from_attributes = True`
        from_attributes = True


# ---------------------------------------------------------------------------
# 3. In-Memory "Database" (for demonstration — use SQLAlchemy in production)
# ---------------------------------------------------------------------------
# In a real app, you'd use SQLAlchemy (async) + PostgreSQL with:
#   - databases library or SQLAlchemy AsyncSession
#   - Alembic for migrations

_students_db: dict[int, dict] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "teacher",
        "is_active": True, "created_at": datetime(2024, 1, 1)},
    2: {"id": 2, "name": "Bob",   "email": "bob@example.com",   "role": "student",
        "is_active": True, "created_at": datetime(2024, 1, 2)},
}
_next_id = 3


# ---------------------------------------------------------------------------
# 4. Dependency Injection
# ---------------------------------------------------------------------------
# Dependencies are callables (functions or classes) that FastAPI resolves
# before calling your route handler. This is how you:
#   - Open a DB connection per request and close it after
#   - Verify a JWT token and inject the current user
#   - Share configuration
#
# FastAPI builds a dependency graph and resolves it in topological order.

def get_db():
    """
    Simulates a database connection dependency.
    In a real app with SQLAlchemy:

        def get_db():
            db = SessionLocal()
            try:
                yield db        ← FastAPI injects this into the handler
            finally:
                db.close()      ← This runs after the handler returns

    The `yield` makes this a generator — FastAPI calls next() to get the
    value, passes it to the handler, then runs the cleanup after.
    """
    return _students_db


def require_admin_role(role: str = Query(default="student")):
    """
    A dependency that simulates auth checking.
    In production, you'd parse a JWT from the Authorization header.
    """
    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required for this endpoint"
        )
    return role


# ---------------------------------------------------------------------------
# 5. Routes — Async Request Handlers
# ---------------------------------------------------------------------------
# `async def` makes this a coroutine. FastAPI runs it in the asyncio event loop.
# Use `async def` when you do I/O (DB queries, HTTP calls, file reads).
# Use `def` (sync) when you do CPU-bound work — FastAPI runs sync handlers
# in a thread pool to avoid blocking the event loop.

@app.get(
    "/",
    summary="Welcome",
    description="Landing page with links to documentation",
    tags=["General"]
)
async def root():
    """
    Simple root endpoint.
    The docstring appears as the endpoint description in /docs.
    """
    return {
        "message": "FastAPI Educational App",
        "docs": "Visit /docs for interactive API documentation",
        "redoc": "Visit /redoc for ReDoc documentation",
    }


@app.get(
    "/students",
    response_model=list[StudentResponse],
    summary="List all students",
    tags=["Students"]
)
async def list_students(
    role: Optional[str] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: dict = Depends(get_db),
):
    """
    List students with optional filters.

    FastAPI automatically:
    - Documents `role` and `is_active` as optional query parameters in /docs
    - Validates their types (is_active must be true/false)
    - Injects the `db` dependency (calls get_db() first)
    - Filters the response through StudentResponse (strips internal fields)
    """
    students = list(db.values())

    if role:
        students = [s for s in students if s["role"] == role]
    if is_active is not None:
        students = [s for s in students if s["is_active"] == is_active]

    return students


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    summary="Get a student by ID",
    tags=["Students"]
)
async def get_student(student_id: int, db: dict = Depends(get_db)):
    """
    Get a single student.

    `student_id: int` in the function signature tells FastAPI:
    1. This is a PATH parameter (because it matches {student_id} in the route)
    2. It must be convertible to int — FastAPI validates this automatically
    3. Document it as a required integer path parameter in /docs

    HTTPException is FastAPI's way to return error responses.
    It sets the status code and formats the detail as JSON: {"detail": "..."}
    """
    student = db.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    return student


@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=201,
    summary="Create a new student",
    tags=["Students"]
)
async def create_student(student: StudentCreate, db: dict = Depends(get_db)):
    """
    Create a student.

    `student: StudentCreate` tells FastAPI:
    1. Parse the request body as JSON
    2. Validate it against StudentCreate's schema
    3. Return 422 with field-level error messages if validation fails
    4. If valid, pass a StudentCreate instance to this function

    This is the "magic" of FastAPI — no manual parsing, no manual validation,
    no manual error messages. The type annotation does all of it.
    """
    global _next_id

    # Check for duplicate email
    if any(s["email"] == student.email for s in db.values()):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_student = {
        "id": _next_id,
        "name": student.name,
        "email": student.email,
        "role": student.role,
        "is_active": True,
        "created_at": datetime.utcnow(),
    }
    db[_next_id] = new_student
    _next_id += 1

    return new_student


@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse,
    summary="Partially update a student",
    tags=["Students"]
)
async def update_student(
    student_id: int,
    updates: StudentUpdate,
    db: dict = Depends(get_db),
):
    """
    PATCH — partial update (only fields provided in the request body).

    `updates.model_dump(exclude_unset=True)` returns only the fields
    that were actually set in the request body, not all fields with
    their defaults. This is a Pydantic v2 pattern for partial updates.
    """
    student = db.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")

    # exclude_unset=True: only include fields the client actually sent
    changes = updates.model_dump(exclude_unset=True)
    student.update(changes)

    return student


@app.delete(
    "/students/{student_id}",
    status_code=204,
    summary="Delete a student",
    tags=["Students"]
)
async def delete_student(student_id: int, db: dict = Depends(get_db)):
    """DELETE a student — returns 204 No Content on success."""
    if student_id not in db:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    del db[student_id]
    # Return None → FastAPI sends an empty 204 response


# ---------------------------------------------------------------------------
# 6. Demonstrating Async — Why It Matters
# ---------------------------------------------------------------------------

@app.get("/async-demo", tags=["Demo"])
async def async_demo():
    """
    Demonstrates why async matters for I/O-heavy workloads.

    In a WSGI app (Flask/Django), `time.sleep(1)` blocks the entire thread.
    Other requests must wait in queue.

    With `await asyncio.sleep(1)`, the event loop suspends THIS coroutine
    and can process other incoming requests during that 1 second.

    Real-world equivalent: awaiting a database query or HTTP API call.
    """
    start = asyncio.get_event_loop().time()
    await asyncio.sleep(5)  # Simulates a 5 second DB query — non-blocking (change to 0.1 for production)
    elapsed = asyncio.get_event_loop().time() - start

    return {
        "message": "This handler yielded control during I/O",
        "elapsed_seconds": round(elapsed, 3),
        "note": (
            "While this coroutine was 'sleeping', uvicorn's event loop "
            "could handle hundreds of other requests concurrently."
        )
    }


# ---------------------------------------------------------------------------
# 7. Middleware in FastAPI
# ---------------------------------------------------------------------------
# FastAPI/Starlette middleware is true ASGI middleware — it wraps the entire
# app as an async callable. Every request passes through all middleware.

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Adds an X-Response-Time header to every response.

    BEHIND THE SCENES:
    Starlette middleware uses the ASGI `call_next` pattern:
    - `await call_next(request)` passes control to the next middleware
      or the actual route handler
    - Code BEFORE call_next runs before the handler (like before_request in Flask)
    - Code AFTER call_next runs after the handler (like after_request in Flask)

    This is more powerful than Flask's hooks because it wraps the response
    object and can modify streaming responses.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response: Response = await call_next(request)
        duration_ms = (time.perf_counter() - start_time) * 1000
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        print(f"[FastAPI] {request.method} {request.url.path} → {response.status_code} ({duration_ms:.1f}ms)")
        return response


app.add_middleware(TimingMiddleware)


# ---------------------------------------------------------------------------
# 8. Startup and Shutdown Events (Lifespan)
# ---------------------------------------------------------------------------
# In FastAPI, you use the `lifespan` context manager (or @app.on_event in older style)
# to run setup/teardown logic around the entire application lifecycle.
# Common uses: create DB connection pool on startup, close it on shutdown.

from contextlib import asynccontextmanager

# (Shown here as a comment to keep the app simple — uncomment to use)
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Starting up: initializing DB connection pool...")
#     # db_pool = await create_pool(DATABASE_URL)
#     yield  # App runs here
#     print("Shutting down: closing DB connection pool...")
#     # await db_pool.close()
#
# app = FastAPI(lifespan=lifespan, ...)


# ---------------------------------------------------------------------------
# 9. AUTH EXERCISE (Uncomment for Chapter 4 of the Lab)
# ---------------------------------------------------------------------------
# UNCOMMENT FOR AUTH EXERCISE - Add these imports at top of file:
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#
# UNCOMMENT FOR AUTH EXERCISE - Add after imports:
# security = HTTPBearer()
#
# UNCOMMENT FOR AUTH EXERCISE - Add this dependency function:
# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     """Simple token auth - in production, validate JWT"""
#     if credentials.credentials != "secret-token":
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return {"username": "testuser", "token": credentials.credentials}

# UNCOMMENT FOR AUTH EXERCISE - Add this protected endpoint:
# @app.get("/protected", tags=["Auth"])
# async def protected_endpoint(user: dict = Depends(get_current_user)):
#     """This endpoint requires Bearer token authentication"""
#     return {"message": f"Hello {user['username']}, you accessed protected data!", "your_token": user['token']}


# ---------------------------------------------------------------------------
# RUN INSTRUCTIONS (do not use app.run() — FastAPI uses uvicorn)
# ---------------------------------------------------------------------------
# uvicorn main:app --reload --port 8000
#
# `main` = this file (main.py)
# `app`  = the FastAPI() instance defined at the top
# --reload  = restart on file changes (dev only)
#
# Visit http://localhost:8000/docs for the interactive Swagger UI
