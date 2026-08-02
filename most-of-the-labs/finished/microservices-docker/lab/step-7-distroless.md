# Step 7 — Distroless images

Replace the alpine runtime with a distroless image: no shell, no package manager, non-root user.

## Do

1. Rewrite `services/users-service/Dockerfile` as a **multi-stage build**.

   **Build stage** (alias it `build`):
   - Base image: `node:20-alpine`
   - Set working directory to `/app`
   - Copy `package*.json`, run `npm install --omit=dev`
   - Copy `server.js`

   **Runtime stage** (no alias — this is the final image):
   - Base image: `gcr.io/distroless/nodejs20-debian12:nonroot`
   - Set working directory to `/app`
   - Copy `/app` from the `build` stage into `/app`, chowning to the `nonroot` user
   - Switch to the `nonroot` user (`USER nonroot`)
   - Expose port `3000`
   - Set the command to `["server.js"]` — **not** `["node", "server.js"]`

   > The distroless `nodejs` image has `node` as its `ENTRYPOINT`, so `CMD` only needs to provide the script path. Using `["node", "server.js"]` would run `node node server.js` and fail.

2. Do the same for `services/products-service/Dockerfile` (the only difference is which directory you're working in).

3. Rebuild:

```bash
docker compose up -d --build
```

## Verify

API still works:

```bash
curl http://localhost:8080/api/users
```

No shell in the image:

```bash
docker compose exec users-service sh
```

Expect `executable file not found`.

Runs as non-root:

```bash
docker inspect $(docker compose ps -q users-service) --format '{{.Config.User}}'
```

Expect `nonroot`.

## Reference

```bash
git diff solution -- services/users-service/Dockerfile services/products-service/Dockerfile
```

---

[← Step 6](./step-6-network-segmentation.md) · [Back to lab index](./README.md)

## You're done

Compare your full repo against the reference:

```bash
git diff solution --stat
```

Final tear-down:

```bash
docker compose down -v
```
