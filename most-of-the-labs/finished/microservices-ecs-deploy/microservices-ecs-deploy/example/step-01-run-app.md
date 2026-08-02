# Step 01 — Run the provided app

**Goal:** start a simple MongoDB container, then run the **provided** Movie API against it by passing the connection string as an environment variable. Confirm the app starts and the endpoints work.

You do **not** write any application code in this step — the app is given to you in [`../movie-api/`](../movie-api/). You only run it.

---

## 1. Start a MongoDB container

A single-container MongoDB is all you need for local development.

```bash
docker run -d --name mongo -p 27017:27017 mongo:7
```

Check it is up:

```bash
docker ps --filter name=mongo
```

---

## 2. Install the app's dependencies

```bash
cd movie-api

python -m venv .venv
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1
                                 # Windows (cmd):        .venv\Scripts\activate.bat

pip install -r requirements.txt
```

---

## 3. Run the app, passing MONGO_URI as an env var

The app reads its database connection from the `MONGO_URI` environment variable. Point it at the MongoDB container you just started (exposed on `localhost:27017`):

```bash
# macOS / Linux
export MONGO_URI="mongodb://localhost:27017/movies"
uvicorn app.main:app --host 0.0.0.0 --port 3000
```

```powershell
# Windows PowerShell
$env:MONGO_URI = "mongodb://localhost:27017/movies"
uvicorn app.main:app --host 0.0.0.0 --port 3000
```

On startup you should see the app confirm the connection:

```
[db] connected to mongodb://localhost:27017/movies
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:3000
```

> If you skip `MONGO_URI`, the app falls back to the same default (`mongodb://localhost:27017/movies`). Setting it explicitly is good practice — and it is exactly how you will configure the app in every later step (Docker `-e`, a ConfigMap/Secret, then Helm values).

---

## 4. Try the endpoints

In a second terminal:

```bash
# health probe
curl http://localhost:3000/health
# {"status":"ok"}

# create a movie
curl -X POST http://localhost:3000/movies \
  -H "Content-Type: application/json" \
  -d '{"title":"Inception","year":2010,"genre":"Sci-Fi"}'
# {"title":"Inception","year":2010,"genre":"Sci-Fi","id":"..."}

# list movies
curl http://localhost:3000/movies

# delete a movie (use the id from the create/list response)
curl -i -X DELETE http://localhost:3000/movies/<id>
# HTTP/1.1 204 No Content
```

You can also open the interactive docs in a browser: **http://localhost:3000/docs**

---

## What you learned

- The app is configured entirely through the `MONGO_URI` environment variable — no code change needed to point it at a different database. This is the single idea every later step reuses.

## Next

→ [Step 02 — Containerize with Docker](step-02-docker.md)
