# Step 02 — Containerize with Docker

**Goal:** write a `Dockerfile` for the provided app **yourself**, build an image, run it as a container against a MongoDB container, and push the image to Docker Hub.

You are **not** given a `Dockerfile` and you are **not** given the commands. Work them out from the requirements and hints below. The only piece of code that is fixed is how the app is started inside the container — see the hint in the CMD section.

> **Set up:** the provided app lives in `movie-api/` (unzip `movie-api-v1.zip` if you don't have it — this step uses the **v1** app; v2 arrives in Step 04.5). The `Dockerfile` and `.dockerignore` you write in this step go **inside `movie-api/`**, next to `requirements.txt` and `app/`, and you build from there. Tag the image `:1.0`. (Reference answer: `solved/step-02/`.)

---

## A. Write a `.dockerignore`

**Why:** your local virtualenv (`.venv`), Python caches (`__pycache__`, `*.pyc`), and git metadata should never go into the image — they bloat it and can leak local state.

**Task:** create a `.dockerignore` in `movie-api/` that excludes those, plus the `Dockerfile`/`.dockerignore` themselves and markdown files.

*Hint:* the syntax is one glob pattern per line, just like `.gitignore`.

---

## B. Write the `Dockerfile`

Build it up directive by directive. For each requirement below, figure out **which Dockerfile instruction** does the job and what its argument should be. Don't copy a finished file — reason about each line.

| # | Requirement | Hint (which instruction?) |
|---|-------------|---------------------------|
| 1 | Start from a small Python 3.12 base image | the instruction that sets the parent image; look for a `-slim` Python tag |
| 2 | Set the working directory to `/app` inside the image | the instruction that changes the build/run directory |
| 3 | Make Python logs appear immediately (unbuffered) and define the listening port | the instruction that sets environment variables; you need `PYTHONUNBUFFERED` and `PORT` |
| 4 | Install dependencies **before** copying the source, for layer caching | copy *only* `requirements.txt`, then the instruction that runs a command at build time to `pip install` it |
| 5 | Copy the application package into the image | the instruction that copies files; copy the `app` directory |
| 6 | Create and switch to a non-root user | a build-time command to add a user, then the instruction that sets the active user |
| 7 | Document the port and define the start command | the instruction that records the exposed port, and the instruction that sets the default process |

**The one fixed piece — how to start the app.** Inside the container the app is launched with an ASGI server:

```
uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
```

*Hint:* use the **shell form** of the start instruction (not the JSON-array/exec form) so that `${PORT}` is expanded by the shell at runtime. If you use the exec form, `${PORT}` will be treated as a literal string.

*Self-check questions:*
- Why copy `requirements.txt` and install **before** `COPY app`? (What does it do to rebuild times when you change only source code?)
- Why run as a non-root user?
- What is the difference between the shell form and the exec form of the start instruction here?

---

## C. Build the image

**Task:** build an image from the `Dockerfile` and tag it `<dockerhub-user>/movie-api:1.0`.

*Hints:*
- The build subcommand of `docker` takes a `-t` flag for the tag and a build-context path (use `.` from inside `movie-api/`).
- After building, list your images to confirm the tag exists.

---

## D. Run the image against a MongoDB container

The API container and the Mongo container must be able to find each other by name. On a **user-defined Docker network**, container names resolve as hostnames.

**Tasks (work out the exact commands):**
1. Create a user-defined Docker network (e.g. `movie-net`).
2. Run a `mongo:7` container **attached to that network**, named `mongo`.
3. Run your API image **on the same network**, publish the container's port `3000` to your host, and pass the database connection string as an **environment variable** so the host part is the Mongo container's name.

*Hints:*
- The network subcommand of `docker` creates networks; `docker run` takes `--network`, `--name`, `-p`/`--publish`, and `-e`/`--env`.
- The value of `MONGO_URI` should look like `mongodb://<mongo-container-name>:27017/movies`. Which name did you give the Mongo container?

**Verify:**
- Curl the `/health` endpoint on the published port.
- Inspect the API container's logs — it should print that it connected to `mongodb://mongo:27017/...`.

*Hint:* `docker logs <container>` shows stdout; `docker ps` shows what's running and the port mappings.

> This is the same name-as-hostname idea Kubernetes Services use — keep it in mind for Step 03.

---

## E. Push to Docker Hub

You will reference this image from Kubernetes next, so it must live in a registry the cluster can pull from.

**Tasks:** authenticate to Docker Hub, then push the tag you built.

*Hints:* there is a `docker` subcommand to log in, and one to push a tagged image. The tag must include your Docker Hub username (you already used it in `-t`).

---

## What you learned

- A `Dockerfile` is an ordered set of instructions; ordering deps before code gives fast, cached rebuilds.
- Containers reach each other by name on a user-defined Docker network — the same idea Kubernetes Services use.

## Next

→ [Step 03 — Deploy to Kubernetes (manual manifests)](step-03-k8s-manual.md)
