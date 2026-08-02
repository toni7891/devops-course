# Step 2 — Both services on a shared network

Run both services in containers on a user-defined network so they can reach each other by name.

## Do

1. Copy your Dockerfile and `.dockerignore` to `services/products-service/`.
2. Build both images:

```bash
docker build -t users-service ./services/users-service
docker build -t products-service ./services/products-service
```

3. Create the network:

```bash
docker network create app-net
```

4. Run both containers:

```bash
docker run -d --name users-service --network app-net -p 3000:3000 \
  -e MONGO_URI=mongodb://host.docker.internal:27017 users-service

docker run -d --name products-service --network app-net -p 3001:3000 \
  -e MONGO_URI=mongodb://host.docker.internal:27017 products-service
```

## Verify

```bash
curl http://localhost:3000/users
curl http://localhost:3001/products
```

Then prove the network works (one container reaches the other by name):

```bash
docker exec users-service node -e "require('http').get('http://products-service:3000/products', r => r.pipe(process.stdout))"
```

Should print products JSON.

## Cleanup before next step

```bash
docker rm -f users-service products-service
docker network rm app-net
```

---

[← Step 1](./step-1-dockerfile.md) · [Next: Step 3 — Replace docker run with Compose →](./step-3-compose.md)
