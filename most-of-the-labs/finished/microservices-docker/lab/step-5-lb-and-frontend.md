# Step 5 — Add the LB and the frontend

Add the Nginx API gateway and the static frontend. Browser hits one origin (`localhost:8080`).

## Do

1. Look at the two existing config files — they're already written for you:
   - `lb/nginx.conf` — routes `/users/*` and `/products/*` to the right service by name
   - `frontend/nginx.conf` — serves static files, proxies `/api/*` to the LB
   - `frontend/public/index.html` — the UI; calls `/api/users` and `/api/products`

2. Create `frontend/Dockerfile`. It must:
   - Use `nginx:alpine` as the base image
   - Copy `nginx.conf` to `/etc/nginx/nginx.conf` inside the image
   - Copy the contents of `public/` to `/usr/share/nginx/html/`
   - Expose port `80`

3. Edit `docker-compose.yml`. Add **two new services**:

   **`lb`** (the load balancer / API gateway)
   - Use the `nginx:alpine` image (no build)
   - Mount the file `./lb/nginx.conf` into the container at `/etc/nginx/nginx.conf` as read-only (`:ro`)
   - `depends_on` both `users-service` and `products-service`
   - Attach to the `app` network
   - **No ports published** — the LB is internal

   **`frontend`** (the static UI)
   - `build:` the `./frontend` directory
   - Publish container port `80` on host port `8080`
   - `depends_on` `lb`
   - Attach to the `app` network

4. **Remove** the `ports:` block from `users-service` and `products-service` — neither needs to be reachable from the host anymore. The browser talks to `frontend`, which proxies to `lb`, which talks to the services internally.

5. Rebuild:

```bash
docker compose down
docker compose up -d --build
```

## Verify

```bash
docker compose ps
```

Expect 6 services Up.

```bash
curl http://localhost:8080/api/users
curl http://localhost:8080/api/products
```

Open <http://localhost:8080> in a browser. Add a user, add a product, click "Buy".

## Reference

```bash
git diff solution -- docker-compose.yml frontend/Dockerfile
```

---

[← Step 4](./step-4-mongo-containers.md) · [Next: Step 6 →](./step-6-network-segmentation.md)
