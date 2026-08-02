# Lab 08 — Secrets & Environment Variables in CI

## Goal

Build a GitHub Actions CI pipeline for a FastAPI + MongoDB app where the
**MongoDB connection URI is never hardcoded** — it is assembled at runtime
from environment variables, and the sensitive parts come from **GitHub
repository Secrets**, not from committed files.

By the end you will have a two-job pipeline:

1. **`unit`** — runs `pytest` against an in-memory Mongo. Needs **no secrets**.
2. **`live`** — starts the real server, points it at a **real MongoDB Atlas
   cluster** using injected secrets, and runs an end-to-end smoke test.

## Learning Objectives

- Understand why credentials must never be committed (`.env` is git-ignored).
- Build a connection string dynamically from individual env vars.
- Store credentials as **GitHub Actions Secrets**.
- Inject secrets into a workflow via `${{ secrets.* }}` and the `env:` block.
- Separate a secret-free test job from a secret-dependent integration job.
- Use `needs:` to chain jobs and `if: always()` for cleanup/diagnostics.

## Prerequisites

- Python 3.12
- A GitHub account + a repo you own (push access)
- A free **MongoDB Atlas** cluster (M0 tier is fine)
- `git`, and a terminal

---

## Part 0 — Get the Code Running Locally

```bash
git clone <your-fork-url>
cd lab08-secrets-and-envs

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Run the unit tests (no DB needed — uses `mongomock-motor`):

```bash
pytest
```

Expected: all tests pass. Tests force `APP_ENV=TEST` and swap the real Mongo
client for an in-memory fake (see [tests/test_users.py](tests/test_users.py)).

**Checkpoint 0:** `pytest` is green before continuing.

---

## Part 1 — Understand the Dynamic URI (the core of the lab)

Open [app/config.py](app/config.py). Note:

- No connection string is written in the code.
- Each part is read from an env var: `MONGO_USER`, `MONGO_PASS`,
  `MONGO_HOST`, `MONGO_DB`.
- The URI is built at runtime:

```
mongodb+srv://<MONGO_USER>:<MONGO_PASS>@<MONGO_HOST>/<MONGO_DB>?appName=Cluster0
```

`quote_plus` escapes the user/password so special characters don't break the URI.

Open [.gitignore](.gitignore) — confirm `.env` is listed. **The real
credentials never enter git.** `.env.example` is committed as a template
**with fake values only**.

**Checkpoint 1:** You can explain, in one sentence, why hardcoding the URI or
committing `.env` would be a security failure.

---

## Part 2 — Local Run Against Real MongoDB Atlas

1. In MongoDB Atlas: create a free cluster, a database user, and a database
   named `express-app`. Under Network Access, allow your IP (or `0.0.0.0/0`
   for the lab only).
2. Copy the template and fill REAL values (this file stays local, git-ignored):

```bash
cp .env.example .env
```

```
APP_ENV=DEV
PORT=3000
MONGO_USER=<your atlas user>
MONGO_PASS=<your atlas password>
MONGO_HOST=cluster0.xxxxx.mongodb.net
MONGO_DB=express-app
```

3. Start the server (terminal 1):

```bash
python -m uvicorn app.main:app --port 3000
```

4. Run the live smoke test (terminal 2):

```bash
python scripts/live_test.py
```

Expected: a series of `PASS` lines ending in `All live checks passed`.
The script exercises health → status → create → read → update → delete →
confirm-gone. See [scripts/live_test.py](scripts/live_test.py).

**Checkpoint 2:** `live_test.py` exits 0 against your real Atlas cluster.

---

## Part 3 — Add the Secrets to GitHub

Push your repo to GitHub if you haven't:

```bash
git remote add origin <your-repo-url>
git push -u origin main
```

In GitHub: **Settings → Secrets and variables → Actions → New repository
secret**. Add **four** secrets (names must match exactly):

| Secret name  | Value                                  |
|--------------|----------------------------------------|
| `MONGO_USER` | your Atlas username                    |
| `MONGO_PASS` | your Atlas password                    |
| `MONGO_HOST` | `cluster0.xxxxx.mongodb.net`           |
| `MONGO_DB`   | `express-app`                          |

> Atlas Network Access must allow GitHub runners. For the lab, set
> `0.0.0.0/0`. (In production you'd use a fixed egress IP / VPC peering.)

**Checkpoint 3:** Four secrets exist in the repo settings. Their values are
never shown again — GitHub masks them.

---

## Part 4 — Write the Workflow

Create `.github/workflows/ci.yml`. Build it up from the requirements below.

### 4a — Triggers + workflow-level env

Run on push and PR to `main`. Define **non-secret** config inline; pull the
**secret** values from `${{ secrets.* }}` at the workflow `env:` level so both
jobs can read them:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  APP_ENV: DEV
  PORT: "3000"
  MONGO_USER: ${{ secrets.MONGO_USER }}
  MONGO_PASS: ${{ secrets.MONGO_PASS }}
  MONGO_HOST: ${{ secrets.MONGO_HOST }}
  MONGO_DB: ${{ secrets.MONGO_DB }}
```

> `APP_ENV` and `PORT` are NOT secrets — non-sensitive config goes in plain
> `env:`. Only credentials go through `secrets`.

### 4b — Job `unit` (no secrets needed)

- `runs-on: ubuntu-latest`
- checkout → setup-python 3.12 (`cache: pip`) → `pip install -r requirements.txt`
- run `pytest` with a **step-level** `env: APP_ENV: TEST` override (tests use
  the in-memory DB, so the Mongo secrets are irrelevant here).

```yaml
jobs:
  unit:
    name: Unit tests (in-memory Mongo)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Run pytest
        env:
          APP_ENV: TEST
        run: pytest
```

### 4c — Job `live` (uses the secrets, runs after `unit`)

- `needs: unit` (only runs if unit tests passed)
- same checkout / python / install steps
- **Start server** in the background, save its PID
- **Run live test** — `python scripts/live_test.py`
- **Stop server** with `if: always()` and dump `server.log` for diagnostics

```yaml
  live:
    name: Live server test (Atlas)
    runs-on: ubuntu-latest
    needs: unit
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Start server
        run: |
          python -m uvicorn app.main:app --port "$PORT" --no-access-log > server.log 2>&1 &
          echo $! > server.pid
      - name: Run live test
        run: python scripts/live_test.py
      - name: Stop server
        if: always()
        run: |
          if [ -f server.pid ]; then kill "$(cat server.pid)" || true; fi
          echo "--- server.log ---"
          cat server.log || true
```

**Why two jobs?** Unit tests must pass with zero credentials — proves the
code is testable without secrets. Only after that do we spend a real DB
connection. `needs: unit` enforces the order; `if: always()` guarantees the
server is killed and its log is printed even when the live test fails.

---

## Part 5 — Run It

```bash
git add .github/workflows/ci.yml
git commit -m "Add CI: unit + live jobs with injected Mongo secrets"
git push
```

Open the **Actions** tab. Watch:

1. `unit` runs first, goes green.
2. `live` starts after, connects to Atlas with the injected secrets, runs the
   smoke test, prints `All live checks passed`.

**Checkpoint 5:** Both jobs are green on GitHub.

---

## Acceptance Criteria

- [ ] `pytest` passes locally with no `.env` and no DB.
- [ ] `.env` is git-ignored; only `.env.example` (fake values) is committed.
- [ ] No connection string or credential appears anywhere in tracked files.
- [ ] Four secrets (`MONGO_USER/PASS/HOST/DB`) exist in repo settings.
- [ ] Workflow injects secrets via `${{ secrets.* }}` at `env:` level.
- [ ] `unit` job runs without any secret.
- [ ] `live` job has `needs: unit` and uses the secrets.
- [ ] Stop-server step uses `if: always()` and prints `server.log`.
- [ ] Both jobs green in the Actions tab.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `live` job hangs then fails on `/livez` | Atlas Network Access blocks runner IP — allow `0.0.0.0/0`. |
| `Missing env var: MONGO_USER` | Secret name typo, or secret added to wrong repo/environment. |
| Auth failure connecting to Atlas | Wrong `MONGO_USER`/`MONGO_PASS`, or password needs URL-escaping (the app already does this — re-check the secret value). |
| `unit` job fails | Real code/test bug — fix locally with `pytest` first; secrets are not involved here. |
| Server step "succeeds" instantly but live test fails | Server crashed on startup — read the `--- server.log ---` dump in the Stop server step. |

## Stretch Goals

- Add a `workflow_dispatch:` trigger to run on demand.
- Use a **GitHub Environment** (e.g. `production`) with required reviewers,
  and move the Mongo secrets to that environment.
- Add a step that greps tracked files for `mongodb+srv://` and fails the
  build if a hardcoded URI is ever committed.
- Matrix the `unit` job across Python 3.11 / 3.12.
