# Step 0 — Run on host (no Docker)

Confirm the app works on your host before adding any Docker.

## Do

1. Make sure MongoDB is running on `localhost:27017`.
2. Install dependencies:

```bash
cd services/users-service && npm install && cd ../..
cd services/products-service && npm install && cd ../..
```

3. In terminal 1:

```bash
cd services/users-service
npm start
```

4. In terminal 2 (PowerShell):

```bash
cd services/products-service
$env:PORT=3001; npm start
```

In terminal 2 (bash):

```bash
cd services/products-service
PORT=3001 npm start
```

## Verify

```bash
curl http://localhost:3000/users
curl http://localhost:3001/products
```

Both must return JSON with `"service":"users-service"` or `"service":"products-service"`.

Stop both services (Ctrl-C) before continuing.

---

[Next: Step 1 — Dockerfile for users-service →](./step-1-dockerfile.md)
