# Step 6 — Split into 4 networks

Isolate each tier on its own network so the LB is the only container that bridges zones.

## Do

1. Replace the single `app` network at the bottom of `docker-compose.yml` with **four** networks:

   | Network | Driver | Internal? |
   | --- | --- | --- |
   | `users-net` | bridge | yes |
   | `products-net` | bridge | yes |
   | `edge-net` | bridge | yes |
   | `public-net` | bridge | no |

   > `internal: true` means containers on that network **cannot reach the public internet**. Only `public-net` allows outbound traffic.

2. Update each service's `networks:` list. Each service should belong **only** to the networks listed here:

   | Service | Networks |
   | --- | --- |
   | `users-db` | `users-net` |
   | `products-db` | `products-net` |
   | `users-service` | `users-net`, `edge-net` |
   | `products-service` | `products-net`, `edge-net` |
   | `lb` | `edge-net`, `public-net` |
   | `frontend` | `public-net` |

3. Restart:

```bash
docker compose down -v
docker compose up -d --build
```

## Verify

API still works:

```bash
curl http://localhost:8080/api/users
curl http://localhost:8080/api/products
```

`users-service` cannot see `products-db`:

```bash
docker compose exec users-service node -e "require('dns').lookup('products-db', e => console.log(e ? e.code : 'FOUND'))"
```

Expect `ENOTFOUND`.

`frontend` cannot reach `users-service` directly:

```bash
docker compose exec frontend sh -c "nc -zvw2 users-service 3000"
```

Expect `bad address`.

`lb` can reach both services:

```bash
docker compose exec lb sh -c "nc -zvw2 users-service 3000 && nc -zvw2 products-service 3000"
```

Expect `open ... open`.

## Reference

```bash
git diff solution -- docker-compose.yml
```

---

[← Step 5](./step-5-lb-and-frontend.md) · [Next: Step 7 →](./step-7-distroless.md)
