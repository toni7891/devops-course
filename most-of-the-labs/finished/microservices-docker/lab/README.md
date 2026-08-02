# Dockerize a Microservices App — Lab

Build up a 6-container microservices stack in 8 small steps. Each step is independently runnable. Verify after every step before moving on.

## Prerequisites

- Docker Desktop (Win/Mac) or Docker Engine + Compose plugin (Linux), v20.10+
- For Step 0 only: Node.js 20+ and MongoDB 7 on `localhost:27017`

## Steps

1. [Step 0 — Run on host (no Docker)](./step-0-run-on-host.md)
2. [Step 1 — Dockerfile for users-service](./step-1-dockerfile.md)
3. [Step 2 — Both services on a shared network](./step-2-shared-network.md)
4. [Step 3 — Replace docker run with Compose](./step-3-compose.md)
5. [Step 4 — MongoDB containers (one per service)](./step-4-mongo-containers.md)
6. [Step 5 — Add the LB and the frontend](./step-5-lb-and-frontend.md)
7. [Step 6 — Split into 4 networks](./step-6-network-segmentation.md)
8. [Step 7 — Distroless images](./step-7-distroless.md)

## Reset commands

Between any two steps, when something goes wrong:

```bash
docker compose down -v
docker rm -f $(docker ps -aq) 2>/dev/null
docker network prune -f
```

## Getting the solution

```bash
git checkout solution -- <path/to/file>    # copy one file from the solution
git diff solution -- <path/to/file>         # diff your file against the solution
```
