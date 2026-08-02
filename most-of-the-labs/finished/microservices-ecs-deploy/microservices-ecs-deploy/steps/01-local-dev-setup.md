# Step 01 — Local development setup

**Goal:** get both services' dependencies installed in isolated virtual
environments and confirm every test passes — before you touch Docker or AWS.

You do **not** write any application code in this step — `app.py`,
`requirements.txt`, and `tests/` are **provided** for each service. You only set
up a clean, reproducible local environment and run the tests.

---

## 1. Why a virtualenv?

Each service declares its own `requirements.txt`. Installing those into your
global Python pollutes your system and makes "works on my machine" bugs. A
**virtual environment** is a throwaway, per-project Python with its own
isolated `site-packages`. We create one **per service** so the two services'
dependency sets never collide.

> The `.venv/` directories are already in `.gitignore` — never commit them.

---

## 2. Set up inventory-service

> Python 3.12 is assumed (matches the container base image). Use `python3` on
> macOS/Linux if `python` points at Python 2.

```bash
# macOS / Linux (bash)
cd inventory-service

python -m venv .venv             # create the virtualenv
source .venv/bin/activate        # activate it (prompt shows (.venv))
pip install -r requirements.txt  # install deps INTO the venv
pytest -q                        # expect: 3 passed

deactivate                       # leave the venv when done
cd ..
```

```powershell
# Windows (PowerShell)
cd inventory-service

python -m venv .venv
.\.venv\Scripts\Activate.ps1     # if blocked: Set-ExecutionPolicy -Scope Process RemoteSigned
pip install -r requirements.txt
pytest -q                        # expect: 3 passed

deactivate
cd ..
```

---

## 3. Set up orders-service

Repeat the exact same flow in the other service. It has its own
`requirements.txt` (it additionally needs `requests`), so it needs its **own**
virtualenv.

```bash
# macOS / Linux (bash)
cd orders-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q                        # expect: 4 passed
deactivate
cd ..
```

```powershell
# Windows (PowerShell)
cd orders-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q                        # expect: 4 passed
deactivate
cd ..
```

> **Tests can't find `app`?** If `pytest` reports
> `ModuleNotFoundError: No module named 'app'`, run it as `python -m pytest -q`
> from inside the service folder — that adds the current directory to the import
> path so `from app import app` resolves.

---

## 4. (Optional) Run a service directly

With a service's venv activated you can run it without Docker:

```bash
# inventory-service, venv active:
python app.py            # serves on http://localhost:8080
# in another shell:
curl -s localhost:8080/stock/widget   # {"sku":"widget","quantity":10}
```

`orders-service` needs `INVENTORY_URL` to point at a running inventory; that's
exactly what Compose does for you in [Step 03](03-compose-local.md), so running
orders standalone is rarely worth it.

---

## What you learned

- A virtualenv gives each service an isolated, reproducible dependency set, so
  the two services never collide and "works on my machine" stops being a
  mystery. Every later step builds on a known-green local baseline.

## Checklist

- [ ] `inventory-service/.venv/` exists and `pytest -q` reports **3 passed**
- [ ] `orders-service/.venv/` exists and `pytest -q` reports **4 passed**
- [ ] Neither `.venv/` directory shows up in `git status` (it's gitignored)

## Next

→ [Step 02 — Containerize each service](02-containerize.md)
