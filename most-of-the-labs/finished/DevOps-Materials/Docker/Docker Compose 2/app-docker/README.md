# Todo App — Dockerized (Compose)

Same todo app as `../app-base/`, now running in two containers orchestrated by Docker Compose.

Diff this folder against `../app-base/` to see exactly what Docker adds — only **3 things** changed:

1. `frontend/vite.config.js` proxy target → `http://backend:3000` (Docker service name)
2. New `Dockerfile.dev` in each service folder
3. New `compose.yaml` at the root

Application code is identical.

## Features

- Two containers: `backend` + `frontend`
- Custom bridge network `todo-net`
- Hot reload via bind mounts (edit code on host → container reloads)
- No DB, in-memory only

## Project Structure

```
app-docker/
├── backend/
│   ├── package.json
│   ├── server.js
│   ├── Dockerfile.dev      # NEW
│   └── .dockerignore       # NEW
├── frontend/
│   ├── package.json
│   ├── vite.config.js      # CHANGED: proxy -> http://backend:3000
│   ├── index.html
│   ├── src/{main.jsx, App.jsx, App.css}
│   ├── Dockerfile.dev      # NEW
│   └── .dockerignore       # NEW
└── compose.yaml            # NEW
```

## Quick Start

```bash
docker compose up --build
```

Open http://localhost:5173.

Stop and remove containers:
```bash
docker compose down
```

## How It Works

- Docker Compose creates network `todo-net`
- Both containers join it, can reach each other by **service name**
- Browser → `localhost:5173` → frontend container (Vite)
- Vite proxy `/api/*` → `http://backend:3000` (resolved inside Docker network)

```
[browser] --> localhost:5173 --> [frontend container]
                                         |
                                  proxy /api/*
                                         v
                                 [backend container]
                                  on todo-net
```

## Hot Reload

Bind mounts in `compose.yaml`:
```yaml
volumes:
  - ./backend:/app
  - /app/node_modules
```
- `./backend:/app` → host code synced into container
- `/app/node_modules` → anonymous volume protects container's `node_modules` from host overlay

Edit `backend/server.js` → `node --watch` restarts.
Edit `frontend/src/App.jsx` → Vite HMR updates browser.

## Junior Pitfalls

### 1. The `node_modules` Trap

Bind-mounting `./frontend:/app` overlays the container's `/app` with your host folder. If the host has no `node_modules` (or has wrong-arch ones from your laptop), the container breaks.

**Fix:** anonymous volume `/app/node_modules` shadows the bind mount at that subpath, keeping the container's installed packages.

### 2. Vite Must Bind to `0.0.0.0`

By default Vite listens on `127.0.0.1` (localhost inside the container). Port forward then shows blank page — your laptop can't reach it.

**Fix:** `--host 0.0.0.0` in the CMD (already in `Dockerfile.dev`).

### 3. Why Proxy, Not CORS

Browser only ever talks to Vite (`localhost:5173`) — same origin, no preflight. The proxy runs **inside** the frontend container, so it can resolve the `backend` service name. Your browser cannot resolve `backend` directly — service names only work inside the Docker network.

### 4. `depends_on` Is Not "Wait Until Ready"

`depends_on: [backend]` only guarantees backend **starts first**, not that it's listening. For this lesson it's fine; in production add a healthcheck.

## Useful Commands

```bash
docker compose up --build     # build + start (foreground)
docker compose up -d          # start detached
docker compose logs -f        # follow logs
docker compose ps             # list services
docker compose down           # stop + remove
docker compose down -v        # also remove volumes
```
