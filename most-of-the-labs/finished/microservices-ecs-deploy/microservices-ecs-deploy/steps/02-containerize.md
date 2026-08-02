# Step 02 — Containerize each service

**Goal:** write a `Dockerfile` for `inventory-service` and another for
`orders-service` **yourself**, build an image for each, and smoke-test that they
run.

No `Dockerfile` is provided — this is the exercise. You create
`inventory-service/Dockerfile` and `orders-service/Dockerfile`. Both services
are the same shape, so the two files will look nearly identical.

> **Set up:** each `Dockerfile` goes **inside its service folder**, next to that
> service's `requirements.txt` and `app.py`, and you build from there.

---

## A. Requirements for each Dockerfile

Each `Dockerfile` must:

- [ ] Start `FROM python:3.12-slim` (match the version you used locally)
- [ ] Set a working directory inside the image (e.g. `/app`)
- [ ] Copy `requirements.txt` **first**, then `pip install -r requirements.txt`,
      then copy `app.py` — so dependency layers stay cached when only the app
      code changes
- [ ] Install with `--no-cache-dir` to keep the image small
- [ ] `EXPOSE 8080`
- [ ] Start the app with **gunicorn**, not the Flask dev server

**The one fixed piece — how to start the app.** Inside the container the app is
launched with gunicorn:

```
gunicorn --bind 0.0.0.0:8080 app:app
```

> `gunicorn` is already in both `requirements.txt`. The Flask dev server
> (`python app.py`) is fine for local poking but must never serve in a
> container that ships to ECS.

*Self-check questions:*
- Why copy `requirements.txt` and install **before** `COPY app.py`? (What does
  it do to rebuild times when you change only source code?)
- Why does `--no-cache-dir` make the image smaller?
- Why gunicorn instead of the Flask dev server in a shipped container?

---

## B. Why copy `requirements.txt` before `app.py`?

Docker caches each layer. If you copy everything at once, any change to
`app.py` busts the `pip install` layer and re-downloads every dependency. By
copying and installing requirements **before** the source, the (slow) install
layer is reused on every build where the dependencies didn't change.

---

## C. Build and smoke-test each image

> **Container port vs. host port — read this first.**
> Inside the image the app **always** listens on `8080` — that's what `EXPOSE 8080`
> and `gunicorn --bind 0.0.0.0:8080` set, and it's the same in **both** images.
> You do **not** change that.
>
> What you choose per `docker run` is the **host** port — the left side of
> `-p HOST:CONTAINER`. Two containers can't share the same host port at the same
> time, so to run both side by side you map each to a **different** host port:
>
> | Image | Container port (fixed) | Host port (you pick) | You curl |
> |---|---|---|---|
> | `inventory-service` | `8080` | `8081` | `localhost:8081` |
> | `orders-service`    | `8080` | `8082` | `localhost:8082` |
>
> So `-p 8081:8080` means "send my machine's port **8081** to the container's
> **8080**." The container never knows or cares which host port you picked.

### inventory-service → host port 8081

```bash
docker build -t inventory-service ./inventory-service

# -p 8081:8080  ->  host 8081 maps to the container's 8080
docker run --rm -d --name inventory -p 8081:8080 inventory-service

curl -s localhost:8081/health        # {"status":"ok"}
curl -s localhost:8081/stock/widget  # {"sku":"widget","quantity":10}

docker stop inventory
```

### orders-service → host port 8082

```bash
docker build -t orders-service ./orders-service

# -p 8082:8080  ->  host 8082 maps to the container's 8080
docker run --rm -d --name orders -p 8082:8080 orders-service

curl -s localhost:8082/health        # {"status":"ok"}
```

`orders`' `/orders` route will **503** on its own — it has no inventory to call
yet; that's expected until [Step 03](03-compose-local.md), where Compose wires
the two together.

```bash
docker stop orders
```

> **Why not just use `8080` for both here?** You can run a single container on
> `-p 8080:8080`, but the moment you start the second one on the same host port
> Docker errors with *"port is already allocated."* Picking `8081` and `8082`
> lets both run at once so you can smoke-test them independently. In Step 03,
> Compose publishes only `orders` and puts it back on the host's `8080`.

---

## What you learned

- A `Dockerfile` is an ordered set of instructions; ordering deps before code
  gives fast, cached rebuilds. Running a real WSGI server (gunicorn) instead of
  the dev server is the difference between a toy and something you'd ship.

## Checklist

- [ ] `inventory-service/Dockerfile` exists and `docker build` succeeds
- [ ] `orders-service/Dockerfile` exists and `docker build` succeeds
- [ ] Both images `EXPOSE 8080` and gunicorn binds the **container** to `8080`
- [ ] Inventory runs on host port `8081`; `/health` and `/stock/widget` respond
- [ ] Orders runs on host port `8082`; `/health` responds (and `/orders` 503s for now)
- [ ] Both images run **gunicorn**, not the Flask dev server

## Next

→ [Step 03 — Run both locally with Compose](03-compose-local.md)
