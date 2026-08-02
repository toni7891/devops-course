# Lab: Docker Bind Mounts for React Development

## Goal

Use **bind mounts** to link local source folders (`src`, `public`) into a
development container so code changes hot-reload **without rebuilding the
image**. Also build a production image served by **nginx**.

The solution to this lab lives on the `solution` branch.

---

## Part 1 — Why Docker for development?

Plain workflow: clone repo, install Node 22, `npm ci`, `npm run dev`.
Easy here, painful on complex projects (many install steps, version drift).

A dev container gives a consistent, prebuilt environment with no local
install. The container runs the dev process but looks at *your local files*.

---

## Part 2 — Create `Dockerfile.dev`

Goal: a container that runs the Vite dev server (not a production build).

Requirements:

- Base image `node:22-alpine`
- Working dir `/app`
- Copy `package.json` + `package-lock.json`, then `npm ci`
  (separate layer so deps are cached when only source changes)
- Copy the rest of the source
- Expose port `3000`
- Start the dev server with `CMD`, not `RUN`
  - `RUN` runs at **build** time
  - `CMD` runs at **container start** time

The `start` script is already in `package.json`:
`vite --host 0.0.0.0 --port 3000`. `--host 0.0.0.0` is required or the
server is unreachable from the host.

---

## Part 3 — Build the dev image

```bash
docker build -t react-app:dev -f Dockerfile.dev .
```

---

## Part 4 — Run without bind mounts

```bash
docker run --rm -d -p 3000:3000 react-app:dev
docker ps
docker logs <container_id>
```

Open `localhost:3000` — app runs.

---

## Part 5 — Hot reload fails

Edit `src/App.jsx`, change a text string, save, refresh. **No change.**

Why: at build time `COPY . .` copied the files into the image. The
container reads its own internal copy, not your local files. Even though
Vite supports HMR, the files inside the container never change.

Stop it: `docker stop <container_id>` (`--rm` auto-removes).

---

## Part 6 — Run with bind mounts

```bash
docker run --rm -d -p 3000:3000 \
  -v "$(pwd)/src:/app/src" \
  react-app:dev
```

`-v <host_path>:<container_path>` — left = host, right = container.
The container's `/app/src` now *is* your local `./src`. No rebuild, no
copy. Edit `src/App.jsx`, save — browser updates automatically.

> Bind mount alone is not enough: the process in the container must
> support hot reload (Vite dev server does). On Windows/macOS hosts,
> filesystem events do not cross the mount, so `vite.config.js` enables
> `server.watch.usePolling` — already configured.

Optionally also mount `./public`.

---

## Part 7 — Create the production `Dockerfile` + `nginx.conf`

Requirements for `Dockerfile`:

- Multi-stage build
- Stage 1 `node:22-alpine`: `npm ci`, then `npm run build` → `/app/dist`
- Stage 2 `nginx:alpine`: copy `nginx.conf` to
  `/etc/nginx/conf.d/default.conf`, copy build output to
  `/usr/share/nginx/html`, expose `80`

Requirements for `nginx.conf`:

- Listen on `80`, root `/usr/share/nginx/html`
- SPA fallback: `try_files $uri $uri/ /index.html` so client-side routes
  do not 404
- Cache `/assets/` aggressively, enable gzip

Build and run:

```bash
docker build -t react-app:prod .
docker run --rm -d -p 8080:80 react-app:prod
# localhost:8080
```

---

## Cleanup

```bash
docker stop $(docker ps -q)
docker rmi $(docker images -q)
```

---

## What you learned

- Docker is for development too, not only production
- Bind mounts link local files directly into a container
- No image rebuild per code change
- Hot reload needs **both** a bind mount **and** a process that supports it
- Production: multi-stage build, static bundle served by nginx with SPA fallback
