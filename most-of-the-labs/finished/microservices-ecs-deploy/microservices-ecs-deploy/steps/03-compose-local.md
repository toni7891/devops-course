# Step 03 — Run both locally with Compose

**Goal:** write `docker-compose.yml` **yourself** that runs both containers
together and proves the cross-service call works locally — the same dependency
you'll later prove in production.

No compose file is provided — you write `docker-compose.yml` at the **repo
root**.

---

## A. Requirements for `docker-compose.yml`

Create `docker-compose.yml` at the **repo root**. It has one top-level
`services:` map with exactly two keys — `inventory` and `orders` — and each key
holds that service's config. (No `version:` line; modern Compose ignores it.)
Look up the exact key names in the
[Compose file reference](https://docs.docker.com/reference/compose-file/services/)
as you go.

**The `inventory` service must:**

- [ ] Set `build:` to `./inventory-service` (the folder with its `Dockerfile`)
- [ ] Have **no** `ports:` — it is not exposed to your host, only to `orders`

**The `orders` service must:**

- [ ] Set `build:` to `./orders-service`
- [ ] Under `ports:`, map `"8080:8080"` (host `8080` → the container's `8080`)
- [ ] Under `environment:`, set `INVENTORY_URL: http://inventory:8080`
- [ ] Under `depends_on:`, list `inventory`

Optionally, give either service a `container_name:` to make `docker compose logs`
and `docker ps` easier to read (otherwise Compose names them like
`microservices-ecs-deploy-orders-1`).

---

**Why each `orders` key is there:**

- **`ports: "8080:8080"`** — the app inside the container listens on `8080`
  (from Step 02). You only publish `orders` because that's the one service *you*
  curl; `inventory` is reached *by `orders`*, not by you. Leaving `inventory`
  with no `ports:` mirrors production, where it's private and only `orders` sits
  behind the load balancer.
  > Unlike Step 02 — where you ran both standalone and picked *different* host
  > ports (`8081`, `8082`) to avoid a collision — here only `orders` publishes,
  > so it can take the clean `8080`.

- **`environment: INVENTORY_URL`** — `orders` reads this exact variable to find
  inventory. See [orders-service/app.py](../orders-service/app.py):
  ```python
  INVENTORY_URL = os.environ.get("INVENTORY_URL", "http://inventory:8080")
  ```
  Setting it in compose makes the wiring explicit instead of relying on the
  code default.
  > **Why the hostname `inventory`?** Compose puts both containers on one network
  > and gives each a DNS name equal to its **service name**. So `orders` reaches
  > the other container at `http://inventory:8080`. This mirrors ECS Service
  > Connect, where the same call becomes `http://inventory.microsvc.local:8080` —
  > same idea, different DNS namespace.

- **`depends_on: inventory`** — starts `inventory` before `orders`.
  > It only waits for the container to **start**, not for the app to be ready to
  > serve. That's fine here — `orders` calls inventory on demand and the 503 path
  > (Section C) handles inventory being briefly unreachable.

*Self-check questions:*
- Why does `inventory` **not** publish a host port, while `orders` does?
- If you renamed the `inventory` service, what else would have to change?
  (Hint: look at `INVENTORY_URL`.)

---

## B. Run it

```bash
docker compose up --build -d

curl -sX POST localhost:8080/orders -H 'content-type: application/json' \
     -d '{"sku":"widget","quantity":2}'    # expect status "confirmed"
curl -sX POST localhost:8080/orders -H 'content-type: application/json' \
     -d '{"sku":"gadget","quantity":2}'    # expect status "backordered"

docker compose logs orders                 # see the request hit inventory
docker compose down
```

`widget` has quantity 10 (≥ 2 → **confirmed**); `gadget` has quantity 0
(< 2 → **backordered**). If both behave as described, your two containers are
talking to each other over the compose network.

---

## C. Prove the dependency locally (optional but recommended)

Stop just inventory and watch orders fail loudly:

```bash
docker compose up --build -d
docker compose stop inventory
curl -isX POST localhost:8080/orders -H 'content-type: application/json' \
     -d '{"sku":"widget","quantity":1}'    # expect HTTP 503
docker compose down
```

This is the exact failure mode you'll reproduce in production in
[Step 08](08-deploy-and-verify.md). If it does **not** return `503`, your
`orders` app is swallowing the connection error instead of surfacing it.

---

## What you learned

- Containers reach each other by **service name** on the compose network — the
  same name-as-hostname idea ECS Service Connect uses. Proving the cross-service
  call (and its failure mode) locally means every later failure is a deploy
  problem, not an app problem.

## Checklist

- [ ] `docker-compose.yml` exists at the repo root with `inventory` + `orders`
- [ ] `orders` has `INVENTORY_URL`, `depends_on: [inventory]`, and publishes `8080`
- [ ] `inventory` does **not** publish a host port
- [ ] `widget` → `confirmed`, `gadget` → `backordered`
- [ ] Stopping inventory makes `/orders` return `503`

## Next

→ [Step 04 — Prepare the GitHub repo](04-github-repo.md)
