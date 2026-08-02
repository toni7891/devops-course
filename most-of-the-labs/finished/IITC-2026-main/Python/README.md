# Python Web Frameworks — Flask vs Django vs FastAPI

A hands-on educational comparison for students learning backend development.

> **New here?** Open **[START_HERE.md](START_HERE.md)** for a step-by-step guide through all the labs.

---

## TL;DR — Which framework should I use?

| | Flask | Django | FastAPI |
|---|---|---|---|
| **Best for** | Small APIs, learning, microservices | Full web apps, CMS, admin panels | High-performance APIs, async workloads |
| **Learning curve** | Low | High | Medium |
| **Batteries included** | No (micro) | Yes (full-stack) | No (but type-safe) |
| **Async support** | Limited | Partial (3.1+) | Native (built-in) |
| **Auto docs** | No | No (third-party) | Yes (Swagger + ReDoc) |
| **ORM** | None built-in | Yes (Django ORM) | None built-in (use SQLAlchemy) |
| **Performance** | Medium | Medium | High |
| **Protocol** | WSGI | WSGI / ASGI | ASGI |

### 🧪 Testing Lab Available!
- See `LAB_Testing.md` for pytest tutorials for all three frameworks
- Covers fixtures, mocking, async testing, and best practices

### ⚡ Performance & Processes Lab Available!
- See `LAB_Performance_Processes.md` for Linux process/thread monitoring
- Covers `ps`, `top`, `pidstat`, multiprocessing vs threading, load testing

### 🚀 Load Testing Comparison Lab Available!
- See `LAB_Load_Testing_Comparison.md` for head-to-head performance battles
- Compare Flask vs Django vs FastAPI with real load tests (`ab`, `wrk`, `locust`)
- Includes automated comparison scripts

---

## The Core Difference: WSGI vs ASGI

### WSGI (Web Server Gateway Interface) — Flask & Django (classic)
```
Browser → Web Server (nginx) → WSGI Server (gunicorn) → Your App (Flask/Django)
```
- **Synchronous**: one request is handled at a time per worker
- Each request blocks the thread until it completes
- To handle 100 concurrent users → need 100 workers (processes/threads)
- Simple mental model, easy to debug

### ASGI (Asynchronous Server Gateway Interface) — FastAPI & Django (new)
```
Browser → Web Server (nginx) → ASGI Server (uvicorn) → Your App (FastAPI)
```
- **Asynchronous**: one worker can juggle many requests using `async/await`
- While waiting for DB/network, the worker handles other requests
- Can handle thousands of concurrent users with far fewer workers
- More complex mental model (event loop, coroutines)

---

## Framework Philosophy

### Flask — "Explicit is better than implicit"
- You choose and wire up every component (ORM, auth, validation, etc.)
- Framework never forces a project structure on you
- Great for understanding how web frameworks actually work
- Risk: inconsistent architecture across projects

### Django — "Batteries included"
- Everything comes pre-wired: ORM, admin panel, auth, forms, templates
- Enforces strong conventions (models.py, views.py, urls.py)
- Great for shipping full-featured apps fast
- Risk: opinionated, heavy for simple use cases

### FastAPI — "Fast to build, fast to run"
- Built on Python type hints — validation, serialization, and docs come "for free"
- Native async — designed for modern I/O-heavy workloads
- Auto-generates Swagger UI and OpenAPI schema
- Risk: ecosystem is younger, some things require more manual setup

---

## Project Structure

```
Python/
├── README.md               ← You are here
├── flask_app/
│   ├── app.py              ← Everything in one file (Flask style)
│   ├── templates/          ← Jinja2 HTML templates
│   └── requirements.txt
├── django_app/
│   ├── manage.py           ← Django CLI entry point
│   ├── config/             ← Project-level settings & root URL conf
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── api/                ← A Django "app" (reusable component)
│       ├── models.py       ← ORM models (DB tables as Python classes)
│       ├── views.py        ← Request handlers
│       └── urls.py         ← URL routing for this app
└── fastapi_app/
    ├── main.py             ← Everything + auto-docs out of the box
    └── requirements.txt
```

---

## Running Each App

> **Python 3.14 Required:** These labs require Python 3.14. Check with `python3 --version`
> If you have a different version, install Python 3.14 from python.org
>
> **macOS users:** You must use a virtual environment (`venv`).
> macOS protects its system Python and blocks direct `pip install`.
>
> **Windows users:** Use **Git Bash** (comes with Git) for the same commands, or use Command Prompt with these changes:
> - Replace `python3` with `python`
> - Replace `source venv/bin/activate` with `venv\Scripts\activate`

---

### What is a virtual environment?
A `venv` is an isolated Python installation just for your project.
It keeps each project's packages separate so they don't conflict.
You create it once, activate it each time you work, then install packages inside it.

---

### Flask
```bash
# 1. Go into the folder
cd flask_app

# 2. Create a virtual environment (creates a folder called venv/)
python3 -m venv venv

# 3. Activate it  ← you must do this every time you open a new terminal
source venv/bin/activate

# Your prompt will change to: (venv) ...  ← this means it's active

# 4. Install dependencies inside the venv
pip install -r requirements.txt

# 5. Run the app
python3 app.py
# Visit: http://localhost:5000

# To deactivate the venv when you're done:
# deactivate
```

**Learn Flask features:**
- See `flask_app/LAB_Flask_Features.md` for hands-on exercises covering Routing, Templates, Manual Validation, and Blueprints
- Includes uncomment exercises for marshmallow validation and blueprint organization

---

### Django
```bash
cd django_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create migration files (required first time!)
python3 manage.py makemigrations

# Apply migrations (creates database tables)
python3 manage.py migrate

# (Optional) Create an admin user to explore /admin/
python3 manage.py createsuperuser

python3 manage.py runserver
# Visit: http://localhost:8000
# Admin: http://localhost:8000/admin/
```

**Learn Django features:**
- See `django_app/LAB_Django_Features.md` for hands-on exercises covering ORM, Admin, Auth, and Routing
- Run `python3 manage.py shell < demo_script.py` to see all features in action

---

### FastAPI
```bash
cd fastapi_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload
# Visit:      http://localhost:8000
# Docs (Swagger UI): http://localhost:8000/docs
# Docs (ReDoc):      http://localhost:8000/redoc
```

**Learn FastAPI features:**
- See `fastapi_app/LAB_FastAPI_Features.md` for hands-on exercises covering Auto Docs, Type Validation, Async, and Dependency Injection
- Features commented code sections for layered learning (uncomment as you progress)

---

### Quick Reference — venv commands

| Action | Command |
|---|---|
| Create venv | `python3 -m venv venv` |
| Activate (macOS/Linux) | `source venv/bin/activate` |
| Activate (Windows) | `venv\Scripts\activate` |
| Check it's active | prompt shows `(venv)` |
| Install packages | `pip install -r requirements.txt` |
| Deactivate | `deactivate` |
| Delete and start fresh | `rm -rf venv/` then create again |
