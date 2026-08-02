# Lab: Containerize a React + TypeScript App with a Distroless Multi-Stage Build

## Objective

Reproduce a production Docker setup for a Vite-built React app. You will write a two-stage Dockerfile: a Node build stage that compiles the app, and a minimal **distroless** runtime stage that serves the static `dist/` output with a tiny zero-dependency Node HTTP server.

## Prerequisites

- Docker installed and running
- A Vite React + TypeScript app with:
  - `npm run build` producing a `dist/` folder
  - A `server.mjs` static file server at the project root

## Background

A multi-stage build keeps the final image small and secure:

- **Build stage** — uses `node:22-slim`, installs all deps (incl. devDeps), runs the build.
- **Runtime stage** — uses `gcr.io/distroless/nodejs22-debian12`. No shell, no package manager, no extra binaries. Only the Node runtime + your built assets. Smaller attack surface, smaller image.

The distroless image has **no shell**, so `CMD` must be exec form pointing directly at the script. The image's entrypoint is `node`, so `CMD ["server.mjs"]` runs `node server.mjs`.

## Steps

### Step 1 — Static file server

Project root needs `server.mjs`. Zero dependencies, serves `dist/` with SPA fallback.

```js
import { createServer } from 'node:http'
import { readFile } from 'node:fs/promises'
import { extname, join, normalize } from 'node:path'

const PORT = process.env.PORT || 8080
const ROOT = join(process.cwd(), 'dist')

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
}

async function sendFile(res, path) {
  const body = await readFile(path)
  res.writeHead(200, { 'content-type': MIME[extname(path)] || 'application/octet-stream' })
  res.end(body)
}

const server = createServer(async (req, res) => {
  try {
    const urlPath = decodeURIComponent((req.url || '/').split('?')[0])
    const safe = normalize(urlPath).replace(/^(\.\.[/\\])+/, '')
    const target = join(ROOT, safe === '/' ? 'index.html' : safe)
    try {
      await sendFile(res, target)
    } catch {
      // SPA fallback
      await sendFile(res, join(ROOT, 'index.html'))
    }
  } catch (err) {
    res.writeHead(500)
    res.end('Internal Server Error')
    console.error(err)
  }
})

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Serving dist/ on http://0.0.0.0:${PORT}`)
})
```

Key points:

- `'0.0.0.0'` bind — required so the container accepts external connections (not just loopback).
- `normalize(...).replace(/^(\.\.[/\\])+/, '')` — path-traversal guard.
- SPA fallback serves `index.html` for unknown routes (client-side routing).

### Step 2 — Build script

`package.json` must build to `dist/`:

```json
{
  "scripts": {
    "build": "tsc -b && vite build",
    "serve": "node server.mjs"
  }
}
```

### Step 3 — Write the Dockerfile

Create `Dockerfile` at project root:

```dockerfile
# build stage
FROM node:22-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# runtime stage — distroless
FROM gcr.io/distroless/nodejs22-debian12 AS runtime
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/server.mjs ./server.mjs
ENV PORT=8080
EXPOSE 8080
CMD ["server.mjs"]
```

Line-by-line:

| Line | Why |
|------|-----|
| `COPY package*.json ./` then `RUN npm ci` before `COPY . .` | Layer caching — deps reinstall only when manifests change |
| `npm ci` | Clean, lockfile-exact install (not `npm install`) |
| `gcr.io/distroless/nodejs22-debian12` | Minimal runtime, no shell/pkg manager |
| `COPY --from=build` | Pulls only `dist/` + `server.mjs` into final image |
| `ENV PORT=8080` | Server reads `process.env.PORT` |
| `CMD ["server.mjs"]` | Exec form. Distroless entrypoint is `node` → runs `node server.mjs` |

### Step 4 — Build the image

```bash
docker build -t react-ts-app .
```

### Step 5 — Run the container

```bash
docker run --rm -p 8080:8080 react-ts-app
```

Expected log:

```
Serving dist/ on http://0.0.0.0:8080
```

### Step 6 — Verify

Open `http://localhost:8080` — React app loads. Test SPA fallback:

```bash
curl -I http://localhost:8080/some/client/route
```

Returns `200` with `index.html` (not 404).

## Verification Checklist

- [ ] `docker build` completes with no errors
- [ ] Final image small (distroless, ~150–200 MB vs ~1 GB+ for full Node)
- [ ] Container starts, prints serving log
- [ ] App reachable at `localhost:8080`
- [ ] Unknown route returns `index.html` (SPA fallback works)
- [ ] `docker image ls react-ts-app` confirms compact size

## Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Container exits immediately | `CMD` uses shell form on distroless (no shell) | Use exec form `["server.mjs"]` |
| Connection refused from host | Server bound to `localhost` not `0.0.0.0` | Bind `'0.0.0.0'` |
| `dist/` not found at runtime | Build stage failed silently or wrong copy path | Check `npm run build` output; verify `COPY --from=build /app/dist` |
| Slow rebuilds | `COPY . .` before `npm ci` | Copy manifests first, install, then copy source |

## Stretch Goals

1. Add a `.dockerignore` (`node_modules`, `dist`, `.git`) to shrink build context.
2. Add a `HEALTHCHECK` — note: distroless has no shell, so use a Node one-liner or an external orchestrator probe.
3. Pin base images by digest (`@sha256:...`) for reproducible builds.
4. Add multi-arch build with `docker buildx build --platform linux/amd64,linux/arm64`.
