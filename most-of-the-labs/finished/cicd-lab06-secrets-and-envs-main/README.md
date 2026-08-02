# express-app (Python port)

Production-like REST API. **Python + FastAPI**, MongoDB (Motor), no auth.

The main thing of this lab is unchanged: the **MongoDB connection URI is
built dynamically from env vars at runtime** — never hardcoded.

## Stack

- FastAPI + uvicorn
- MongoDB via Motor (async PyMongo)
- CORS, gzip, in-process rate limit
- Pydantic validation
- pytest + httpx + mongomock-motor (in-memory Mongo for tests)

## Layout

```
app/
  main.py             # FastAPI app factory + /status + bootstrap (lifespan)
  config.py           # env vars + dynamic Mongo URI   <-- the lab's main thing
  database.py         # motor connect / disconnect
  errors.py           # HttpError
  schemas.py          # pydantic validation
  health.py           # /livez /readyz
  users/              # routes -> service -> store (Motor collection)
tests/                # pytest integration (in-memory Mongo)
```

## Environment

Connection URI is built dynamically from the parts (see [app/config.py](app/config.py)):

| Var          | Meaning                          |
|--------------|----------------------------------|
| `APP_ENV`    | App status: `DEV` or `TEST`      |
| `PORT`       | HTTP service port                |
| `MONGO_USER` | Mongo username                   |
| `MONGO_PASS` | Mongo password                   |
| `MONGO_HOST` | Mongo host (e.g. `cluster0.x.mongodb.net`) |
| `MONGO_DB`   | Database name                    |

URI: `mongodb+srv://<MONGO_USER>:<MONGO_PASS>@<MONGO_HOST>/<MONGO_DB>?appName=Cluster0`

## Run

```bash
cp .env.example .env
python -m venv .venv && .venv/Scripts/activate   # Windows
pip install -r requirements.txt
python -m app.main
```

Needs a reachable MongoDB (Atlas via `MONGO_HOST`, or adjust the URI for local).

## Endpoints

- `GET  /livez`, `GET /readyz`
- `GET  /status`              `{ status: DEV|TEST, port, db }`
- `GET  /api/users`
- `POST /api/users`           `{ name, email }`
- `GET  /api/users/{id}`
- `PATCH /api/users/{id}`     partial `{ name?, email? }`
- `DELETE /api/users/{id}`

## Test

In-memory Mongo, no external DB needed. Test deps included in `requirements.txt`.

```bash
pytest
```
