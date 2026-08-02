# Python Web Frameworks — Student Guide

> **Start here.** This is your roadmap through all the labs.
> Follow the steps in order. Each step builds on the previous one.

---

## Before You Begin

**You need:** Python 3.14 installed. Check with:
```bash
python3 --version
```

**macOS users:** You must use virtual environments (explained below).

**Windows users:** Use Git Bash and replace:
- `python3` → `python`
- `source venv/bin/activate` → `venv\Scripts\activate`

---

## How Virtual Environments Work

Every framework folder has its own `venv`. You create it once, then activate it every time you work.

```bash
# Go into a framework folder
cd flask_app        # (or django_app, or fastapi_app)

# Create the virtual environment (one time only)
python3 -m venv venv

# Activate it (every time you open a new terminal)
source venv/bin/activate

# Your prompt changes to: (venv) ...
# Now install packages
pip install -r requirements.txt

# When you're done:
deactivate
```

> **Rule:** Always activate the venv before running anything inside a framework folder.

---

## Step 1: Learn Flask (Optional — You Already Know This!)

> **You can skip this step** if you already learned Flask in class. Jump to Step 2 (Django).
> This is here as a reference if you want to review or practice.

Flask is the simplest framework.

### Setup
```bash
cd flask_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
# Visit: http://localhost:5000
```

### Lab
Open **[flask_app/LAB_Flask_Features.md](flask_app/LAB_Flask_Features.md)** and work through:

| Chapter | What You Learn |
|---------|---------------|
| 1 | Why Flask — the philosophy |
| 2 | Your first app — routes and responses |
| 3 | Routing and request handling |
| 4 | GET vs POST — HTTP methods |
| 5 | Templates — rendering HTML |
| 6 | Manual validation (compare with FastAPI later) |
| 7 | Blueprints — organizing bigger apps |
| 8 | Testing Flask apps |

---

## Step 2: Learn Django

Django gives you everything built-in: ORM, admin panel, auth system.

### Setup
```bash
cd django_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
# Visit: http://localhost:8000
```

### Lab
Open **[django_app/LAB_Django_Features.md](django_app/LAB_Django_Features.md)** and work through:

| Chapter | What You Learn |
|---------|---------------|
| 1 | What is ORM — the database problem |
| 2 | Your first ORM queries |
| 3 | The magic admin panel |
| 4 | Django architecture (models, views, urls) |
| 5 | Built-in auth system |
| 6 | Testing the API with curl |
| 7 | Unit testing with Django |

---

## Step 3: Learn FastAPI

FastAPI is modern, async, and auto-generates API docs.

### Setup
```bash
cd fastapi_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# Visit: http://localhost:8000
# Docs:  http://localhost:8000/docs
```

### Lab
Open **[fastapi_app/LAB_FastAPI_Features.md](fastapi_app/LAB_FastAPI_Features.md)** and work through:

| Chapter | What You Learn |
|---------|---------------|
| 1 | What makes FastAPI different |
| 2 | Automatic Swagger docs |
| 3 | Type hints = free validation |
| 4 | Dependency injection |
| 5 | Async — why it matters |
| 6 | Testing the API with curl |
| 7 | Testing with pytest |

---

## Step 4: Testing

Now that you know all three frameworks, learn how to test properly.

### Setup
```bash
# From the Python/ root folder — no venv needed for basic pytest
pip install pytest
```

### Lab
Open **[LAB_Testing.md](LAB_Testing.md)** and work through:

| Chapter | What You Learn |
|---------|---------------|
| 1 | pytest basics — assertions, running tests |
| 2 | Testing Flask with the test client |
| 5 | Mocking — faking external services |
| 6 | Test organization best practices |
| 7 | Running tests — useful pytest flags |

### Your first task
Run the broken tests and fix them:
```bash
# From the Python/ folder
pytest test_example.py -v
# You'll see failures — read the errors and fix the code!
```

---

## Step 5: Performance, Processes & Profiling

Understand how Python handles concurrency and how to measure performance.

### Lab
Open **[LAB_Performance_Processes.md](LAB_Performance_Processes.md)** and work through:

| Chapter | What You Learn |
|---------|---------------|
| 1 | Process vs Thread — the restaurant analogy |
| 2 | Linux monitoring commands (`ps`, `top`, `pidstat`) |
| 3 | Python threading vs multiprocessing |
| 4 | Monitor your web apps |
| 5 | Load testing tools (`ab`, `wrk`, Locust) |
| 6 | Profiling (`time`, `cProfile`, `line_profiler`) |
| 7 | Real debugging scenario |

### Demo files to run
```bash
# From the Python/ folder
python3 threading_demo.py    # I/O-bound: threading wins
python3 cpu_demo.py          # CPU-bound: multiprocessing wins
time python3 cpu_demo.py     # Measure it
```

Each file has `# CHALLENGE` comments at the bottom — try them!

---

## Step 6: Load Testing Comparison (Advanced)

Compare all three frameworks head-to-head under load.

### Prerequisites
```bash
# macOS
brew install wrk

# Locust (install in any venv or globally)
pip install locust
```

### Lab
Open **[LAB_Load_Testing_Comparison.md](LAB_Load_Testing_Comparison.md)** and work through:

| Chapter | What You Learn |
|---------|---------------|
| 1 | Test setup — starting all three servers |
| 2 | Basic load test with `ab` |
| 3 | Heavy load test with `wrk` |
| 4 | Realistic scenarios with Locust |
| 5 | Multi-worker test (Gunicorn/Uvicorn) |
| 6 | Understanding the results |
| 7 | Automated comparison script |

---

## Quick Reference

### All Lab Files

| File | What It Covers |
|------|---------------|
| [flask_app/LAB_Flask_Features.md](flask_app/LAB_Flask_Features.md) | Flask routing, templates, validation, blueprints |
| [django_app/LAB_Django_Features.md](django_app/LAB_Django_Features.md) | Django ORM, admin, auth, architecture |
| [fastapi_app/LAB_FastAPI_Features.md](fastapi_app/LAB_FastAPI_Features.md) | FastAPI docs, type hints, async, DI |
| [LAB_Testing.md](LAB_Testing.md) | pytest, mocking, test organization |
| [LAB_Performance_Processes.md](LAB_Performance_Processes.md) | Processes, threads, profiling |
| [LAB_Load_Testing_Comparison.md](LAB_Load_Testing_Comparison.md) | ab, wrk, Locust, framework comparison |

### Demo Files (in Python/ folder)

| File | Purpose |
|------|---------|
| `test_example.py` | Broken tests — fix them to learn pytest |
| `threading_demo.py` | Threading demo for I/O-bound tasks |
| `cpu_demo.py` | Multiprocessing demo for CPU-bound tasks |
| `locustfile.py` | Locust load test config |
| `compare_frameworks.sh` | Automated load test script |
| `monitor_webapp.sh` | Monitor running web apps |

### Default Ports

| Framework | URL |
|-----------|-----|
| Flask | http://localhost:5000 |
| Django | http://localhost:8000 |
| FastAPI | http://localhost:8000 |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `command not found: python3` | Install Python 3.14 from python.org |
| `No module named ...` | Did you activate the venv? Run `source venv/bin/activate` |
| `pip install` fails on macOS | You're not in a venv. Create and activate one first |
| Port already in use | Another server is running. Stop it with `Ctrl+C` or change the port |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside the activated venv |
| Tests fail | Read the error message carefully — that's the exercise! |
