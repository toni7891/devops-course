# Step 4 — MongoDB containers (one per service)

Stop depending on host-installed Mongo. Each service gets its own MongoDB container with a named volume.

## Do

1. Edit `docker-compose.yml`. Add **two new services** under `services:`:

   **`users-db`**
   - Use the `mongo:7` image (no build)
   - Mount a named volume called `users-db-data` at `/data/db` inside the container
   - Attach to the `app` network

   **`products-db`**
   - Same as above but with `mongo:7`, volume name `products-db-data`, same `app` network

2. Change the `MONGO_URI` environment variable on each backend service:

   | Service | New MONGO_URI |
   | --- | --- |
   | users-service | `mongodb://users-db:27017` |
   | products-service | `mongodb://products-db:27017` |

3. Add a `depends_on` field to each backend service so it waits for its DB:
   - `users-service` depends on `users-db`
   - `products-service` depends on `products-db`

4. Add a top-level `volumes:` block at the bottom of the file declaring both named volumes: `users-db-data` and `products-db-data`. (Empty definitions are fine — Compose creates the volumes with defaults.)

5. Restart:

```bash
docker compose down
docker compose up -d --build
```

## Verify

```bash
docker compose ps
```

Expect 4 services Up: `users-db`, `products-db`, `users-service`, `products-service`.

Test that data persists across restarts:

```bash
curl -X POST http://localhost:3000/users \
  -H 'content-type: application/json' \
  -d '{"name":"Ada","email":"a@b.c"}'

docker compose restart users-service
sleep 5
curl http://localhost:3000/users
```

Ada is still there after the restart.

## Reference

```bash
git diff solution -- docker-compose.yml
```

---

[← Step 3](./step-3-compose.md) · [Next: Step 5 →](./step-5-lb-and-frontend.md)
