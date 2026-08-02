# Step 3 — Replace docker run with Compose

Put everything from Step 2 into a single `docker-compose.yml`.

## Do

1. Create `docker-compose.yml` at the repo root. Under a top-level `services:` key, define **two services**:

   **`users-service`**
   - `build:` the `./services/users-service` directory
   - One environment variable: `MONGO_URI` = `mongodb://host.docker.internal:27017`
   - Publish container port `3000` on host port `3000`
   - Attach to a network named `app`

   **`products-service`**
   - `build:` the `./services/products-service` directory
   - Same `MONGO_URI` as above
   - Publish container port `3000` on host port `3001`
   - Attach to the same `app` network

2. Add a top-level `networks:` block at the bottom that declares `app` with `driver: bridge`.

3. Start it:

```bash
docker compose up -d --build
```

## Verify

```bash
docker compose ps
curl http://localhost:3000/users
curl http://localhost:3001/products
```

## Reference

```bash
git checkout solution -- docker-compose.yml
```

> The solution file has more services than you have right now. Look only at how `users-service` and `products-service` are structured for this step.

---

[← Step 2](./step-2-shared-network.md) · [Next: Step 4 →](./step-4-mongo-containers.md)
