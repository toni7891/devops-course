# Lab: Containerize an Express + TypeScript API with a Multi-Stage Distroless Build

## Goal

Write a production-grade `Dockerfile` for this Express 5 + TypeScript app. The
final image must:

- Compile TypeScript at build time (no `tsx`/`ts-node` at runtime).
- Use a **multi-stage** build so build tooling and dev dependencies never reach
  the runtime image.
- Run on a **distroless** base (no shell, no package manager) as a hardening
  measure.
- Expose the app on port `3000` and start it with `node dist/index.js`.

There is intentionally **no `Dockerfile` in this repo** — you create it.

## Background

| Fact | Value |
|------|-------|
| Language | TypeScript (`commonjs`, target ES2022) |
| Build command | `npm run build` (runs `tsc`) |
| Build output | `dist/` (see `tsconfig.json` → `outDir`) |
| Entry point | `dist/index.js` |
| Listen address | `0.0.0.0:3000` (`PORT` env overrides) |
| Health endpoint | `GET /health` → `{"status":"ok"}` |
| Node version | 22.x |

The app binds `0.0.0.0` (not `localhost`) — required so the port is reachable
from outside the container.

## Acceptance Criteria

1. `docker build -t express-ts-app .` succeeds.
2. Build uses at least two `FROM` stages; the final stage is distroless.
3. Runtime image contains **no dev dependencies** (`tsx`, `typescript`,
   `@types/*`) and **no source `.ts` files** — only compiled `dist/` + prod
   `node_modules`.
4. `docker run -p 3000:3000 express-ts-app` starts the server.
5. `curl http://localhost:3000/health` returns `{"status":"ok"}`.
6. Final image size is materially smaller than a naive single-stage
   `node:22` build (target: under ~200 MB).

## Steps

### 1. Build stage

Start from a Node 22 image that includes a toolchain (e.g. `node:22-slim`).

- Set a working directory.
- Copy **only** `package*.json` first, then `npm ci`. (Copying manifests
  before source code keeps the dependency layer cached when only source
  changes.)
- Copy the rest of the source.
- Run `npm run build` to produce `dist/`.
- Strip dev dependencies from `node_modules` so they can be reused in the
  runtime stage: `npm prune --omit=dev`.

### 2. Runtime stage

Start a new stage `FROM gcr.io/distroless/nodejs22-debian12`.

- Distroless has **no shell** — you cannot `RUN npm ...` here. Only `COPY` and
  `CMD`.
- Copy the pruned `node_modules` and the compiled `dist/` from the build stage.
- Set `ENV PORT=3000`, `EXPOSE 3000`.
- The distroless `nodejs` image's entrypoint is already `node`, so `CMD` is
  just the script path: `CMD ["dist/index.js"]`.

### 3. Add a `.dockerignore`

Create `.dockerignore` so local junk never enters the build context:

```
node_modules
dist
.git
*.md
```

### 4. Build, run, verify

```bash
docker build -t express-ts-app .
docker run --rm -p 3000:3000 express-ts-app
# in another terminal:
curl http://localhost:3000/health      # -> {"status":"ok"}
docker images express-ts-app           # check size
```

## Hints

- Distroless tag `gcr.io/distroless/nodejs22-debian12` already sets
  `ENTRYPOINT ["/nodejs/bin/node"]`. Passing `["node","dist/index.js"]` as
  `CMD` would try to run `node node dist/index.js`. Pass only the script.
- Build context too big / slow? Your `.dockerignore` is missing or wrong.
- Can't `docker exec` a shell into the running container? Expected — distroless
  has none. Debug from the build stage instead (`--target build`).
- Layer cache busts on every build? You're copying source before `npm ci`.

## Stretch

- Add a `HEALTHCHECK`. Note distroless has no `curl`/`wget` — use a tiny Node
  one-liner via the image's `node`.
- Pin the base images by digest (`@sha256:...`) for reproducible builds.
- Add a non-root `USER` (distroless ships a `nonroot` user, uid 65532).

## Solution

Reference solution: `Dockerfile.solution` (instructor copy — do not ship to
students).
