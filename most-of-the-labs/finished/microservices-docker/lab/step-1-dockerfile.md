# Step 1 — Dockerfile for users-service

Package `users-service` into a Docker image. Mongo and products-service stay on the host.

## Do

1. Create `services/users-service/.dockerignore`. It should list `node_modules` and `npm-debug.log` (each on its own line).

2. Create `services/users-service/Dockerfile`. The file must:
   - Use `node:20-alpine` as the base image.
   - Set the working directory to `/app`.
   - Copy `package*.json` into the working directory.
   - Run `npm install --omit=dev`.
   - Copy `server.js` into the working directory.
   - Expose port `3000`.
   - Start the container with `node server.js`.

> The order matters: copy `package*.json` and install **before** copying `server.js`. That way changes to `server.js` don't bust the npm-install layer cache.

3. Build the image:

```bash
docker build -t users-service ./services/users-service
```

4. Run the container.

Win/Mac:

```bash
docker run --rm -p 3000:3000 \
  -e MONGO_URI=mongodb://host.docker.internal:27017 \
  users-service
```

Linux:

```bash
docker run --rm -p 3000:3000 --network host \
  -e MONGO_URI=mongodb://localhost:27017 \
  users-service
```

## Verify

```bash
curl http://localhost:3000/users
```

Returns `{"service":"users-service","count":0,"users":[]}`.

Stop the container (Ctrl-C) before continuing.

## Reference

```bash
git diff solution -- services/users-service/Dockerfile
```

---

[← Step 0](./step-0-run-on-host.md) · [Next: Step 2 →](./step-2-shared-network.md)
