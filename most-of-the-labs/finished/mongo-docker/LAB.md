# Lab — Persist MongoDB Data with Docker Named Volumes

> **Working branch:** `main`. The seed script is already provided in
> `docker-entrypoint-initdb.d/01-seed.js` — **do not modify it**. Your job is
> the Docker setup: build an image that runs the seed, persist its data with a
> named volume, and connect with `mongosh`. Stuck? `git checkout solution` for
> the reference, then `git checkout main` and try again yourself.

**The scenario:** Your DevOps team is standardizing the backend team's MongoDB
environment using Docker. The seed data and init script are given. You must
containerize MongoDB so every developer and CI run gets the same seeded
database — and so the data survives container removal.

**Conventions used below:**

- Image name: `mongo-lab-img`
- Container name: `mongo-lab`
- Port: `27017`
- Root user / password: `root` / `secret` (admin only)
- App user / password: `appuser` / `appsecret` (created by the seed, scoped to `appdb`)
- App database: `appdb` (seeded by the provided script)
- Named volume: `mongodata`

**What is provided vs. what you do:**

| Provided (do not change)                 | You build                                   |
| ---------------------------------------- | ------------------------------------------- |
| `docker-entrypoint-initdb.d/01-seed.js`  | `Dockerfile` (currently a stub with TODOs)  |
| This `LAB.md`                            | All `docker` / `docker volume` commands     |
|                                          | The `mongosh` connection                    |

---

## Setup & Prerequisites

Do this before Part 1.

### Tools

- **Docker** — `docker --version` (engine running: `docker info`)
- **mongosh** (MongoDB Shell) — `mongosh --version`. Install:
  <https://www.mongodb.com/docs/mongodb-shell/install/>
  - Alternative: MongoDB Compass (GUI) instead of `mongosh`.

### Get the repo

```bash
git clone <repo-url> mongo-docker
cd mongo-docker
git branch          # you are on `main` — this is your working branch
```

- `main` — your working branch (skeleton: stub `Dockerfile`, provided seed).
- `solution` — reference. `git checkout solution` to peek, then
  `git checkout main` to return. Try yourself first.

### Connection cheat-sheet

```bash
# as root (admin) — Parts 1–5
mongosh "mongodb://root:secret@localhost:27017/?authSource=admin"

# as appuser (scoped to appdb) — Part 6 onward, after the seed runs
mongosh "mongodb://appuser:appsecret@localhost:27017/appdb"
```

---

## Part 1 — Run Stock MongoDB Without Persistence

**Objective:** Get the official `mongo` image running and feel that it is
ephemeral. (No custom image yet — that's Part 5.)

### Instructions

1. Run an official `mongo` container in the background.
2. Configure via flags / environment variables:
   - container name `mongo-lab`
   - publish port `27017`
   - root credentials via `MONGO_INITDB_ROOT_USERNAME` and
     `MONGO_INITDB_ROOT_PASSWORD`
3. Confirm it is running (`docker ps`).
4. Connect with `mongosh` using the root credentials.
5. Manually create database `appdb`, a `products` collection, and 2–3 docs.

<details><summary>Hint — command shape</summary>

```bash
docker run -d --name ___ -p ___:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=___ \
  -e MONGO_INITDB_ROOT_PASSWORD=___ \
  mongo:7
docker ps
```
Then connect with the root cheat-sheet line and `db.getSiblingDB("appdb")`.
</details>

### Verification

- `docker ps` shows `mongo-lab` as `Up`
- `mongosh` connects; `db.products.countDocuments()` returns your count

### Investigation Questions

- Inside the container, which directory does MongoDB write its data files to?
- What does the `MONGO_INITDB_ROOT_*` env config do on first start?

---

## Part 2 — Destroy the Container

**Objective:** Experience data loss firsthand.

### Instructions

1. Stop the `mongo-lab` container.
2. **Remove** it completely (`docker rm`).
3. Run a brand-new `mongo` container with the same settings (still no volume).
4. Reconnect with `mongosh` and look for your `appdb` / `products` data.

<details><summary>Hint — command shape</summary>

```bash
docker stop mongo-lab
docker rm mongo-lab
# run a fresh `mongo` container again (same as Part 1, no -v)
```
</details>

### Verification

- The new container is running
- Your data is **gone**

### Investigation Questions

- Why did the data disappear?
- Where was MongoDB storing the files, and what happened to that storage on
  `docker rm`?
- Are containers designed to hold persistent state? Why / why not?

---

## Part 3 — Add a Named Volume

**Objective:** Make stock MongoDB persistent with Docker-managed storage.

### Instructions

1. Create a named volume called `mongodata`.
2. Run a fresh `mongo` container, mounting `mongodata` at MongoDB's internal
   data path (`/data/db`).
3. Connect with `mongosh` and recreate some sample data.

<details><summary>Hint — command shape</summary>

```bash
docker volume create ___
docker run -d --name mongo-lab -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -v ___:/data/db \
  mongo:7
```
The mount target is MongoDB's data path — see Part 1 investigation.
</details>

### Verification

- `docker volume ls` lists `mongodata`
- Data is queryable

### Investigation Questions

- Why `/data/db` specifically? How did you confirm the correct path?
- Is the volume tied to this container's lifecycle?

---

## Part 4 — Verify Persistence

**Objective:** Prove the volume outlives the container.

### Instructions

1. Stop the container, then **remove** it completely (`docker rm`).
2. Run a **brand-new** `mongo` container mounting the **same** `mongodata`
   volume at `/data/db`.
3. Connect with `mongosh` and check your data.

<details><summary>Hint — command shape</summary>

```bash
docker stop mongo-lab && docker rm mongo-lab
# new container, SAME -v mongodata:/data/db
docker run -d --name mongo-lab -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -v mongodata:/data/db \
  mongo:7
```
</details>

### Verification

- The container was fully removed and recreated
- Your data **still exists**

### Investigation Questions

- What is the key difference between Part 2 and Part 4?
- State, in one sentence, the relationship between containers and volumes.

---

## Part 5 — Build a Custom Image That Auto-Seeds

**Objective:** Stop creating data by hand. Build an image from the provided
`Dockerfile` (currently a stub) that bakes in the **provided** seed script so
MongoDB seeds `appdb` automatically on first start.

### Instructions

1. Inspect `docker-entrypoint-initdb.d/01-seed.js` — this is **provided and
   working**. Do not modify it. Note it seeds `users`, `products`, `orders`
   into `appdb`, **and creates the `appuser` application user** scoped to
   `appdb`.
2. Open `Dockerfile` (a stub with TODOs). Implement it so that:
   - it is based on the official `mongo` image (pin a tag, not `:latest`)
   - it copies the `docker-entrypoint-initdb.d/` directory into the image at
     `/docker-entrypoint-initdb.d/`
3. Build the image: tag it `mongo-lab-img`.
4. Run a container from **your** image. Because init scripts only run on a
   **fresh** data directory, use a **new** named volume (or remove the old
   `mongodata` first).
5. Check `docker logs mongo-lab` for the `Seed complete` output.

<details><summary>Hint — Dockerfile + build</summary>

`Dockerfile`:
```dockerfile
FROM mongo:___
COPY docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/
EXPOSE 27017
```
```bash
docker build -t mongo-lab-img .
docker rm -f mongo-lab; docker volume rm mongodata; docker volume create mongodata
docker run -d --name mongo-lab -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -v mongodata:/data/db mongo-lab-img
docker logs mongo-lab | grep -A3 "Seed complete"
```
Init runs only on a fresh volume — remove the old one first.
</details>

### Verification

- `docker build` succeeds
- `docker logs` shows the seed counts (users: 3, products: 4, orders: 3)

### Investigation Questions

- Why pin a specific `mongo` tag instead of `latest`?
- Why must the volume be *fresh* for the seed to run? (Relate to Parts 3–4.)
- What is the load order if there are multiple init scripts? (Hint: the `01-`
  prefix.)

---

## Part 6 — Connect and Explore the Seeded Data

**Objective:** Use `mongosh` to confirm the auto-seeded e-commerce data, and
connect as the least-privilege `appuser` the seed created.

### Instructions

1. Connect to `appdb` with `mongosh` as **`appuser`** (not root). The seed
   created this user scoped to `appdb` with `readWrite`.
2. Run queries to confirm the seed:
   - count documents in `users`, `products`, `orders`
   - find one order and trace its `userId` / `productId` references back to
     the `users` and `products` collections
3. Try a privileged action outside `appdb` (e.g. list databases or write to
   another DB) and observe `appuser` is denied.

<details><summary>Hint — command shape</summary>

```bash
mongosh "mongodb://appuser:appsecret@localhost:27017/appdb" --eval '
  print(db.users.countDocuments());
  const o = db.orders.findOne();
  printjson(db.users.findOne({_id: o.userId}));
'
# least-privilege check — expect "not authorized":
mongosh "mongodb://appuser:appsecret@localhost:27017/appdb" --eval '
  db.getSiblingDB("otherdb").x.insertOne({a:1});
'
```
</details>

### Verification

- `appuser` connects to `appdb` successfully
- `db.users.countDocuments()` → 3
- `db.products.countDocuments()` → 4
- `db.orders.countDocuments()` → 3
- You can resolve an order's references to a real user and real products
- `appuser` is rejected when acting outside `appdb`

### Investigation Questions

- Why connect as `appuser` instead of root? What is least privilege?
- Did you have to insert any data by hand this time? Why not?
- If you `docker rm` this container and recreate it on the **same** volume,
  will the seed run again? Will the data still be there? (Explain both.)

---

## Part 7 — Inspect Docker Volumes

**Objective:** Understand where and how Docker stores volume data.

### Instructions

1. List all Docker volumes.
2. Inspect the volume backing your seeded container.
3. Identify the **name**, **mountpoint**, and **driver**.
4. Research: on a Linux Docker host, which directory holds named-volume data?

<details><summary>Hint — command shape</summary>

```bash
docker volume ls
docker volume inspect mongodata
```
Read the `Mountpoint` and `Driver` fields from the JSON output.
</details>

### Verification

- You can state the mountpoint and driver for the volume

### Investigation Questions

- Why is the mountpoint *Docker-managed* rather than a path you chose?
- On Docker Desktop (Windows/macOS), where does this data physically live?

---

## Part 8 — Bind Mounts vs Named Volumes

**Objective:** Compare the two persistence mechanisms.

### Instructions

1. Run a container from your image using a **bind mount** to a host path
   (e.g. the `mongo-init/` directory or another host folder) for `/data/db`
   instead of a named volume.
2. Inspect the host directory — note you can browse the files directly.
3. Compare with the named-volume behavior from Parts 3–7.

<details><summary>Hint — command shape</summary>

```bash
mkdir -p ./hostdata
docker rm -f mongo-lab
docker run -d --name mongo-lab -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -v "$(pwd)/hostdata:/data/db" \
  mongo-lab-img
ls -la ./hostdata    # MongoDB files now visible on the host
```
PowerShell: replace `$(pwd)` with `${PWD}`.
</details>

### Comparison

| Bind Mount                  | Named Volume                 |
| --------------------------- | ---------------------------- |
| Good for development access | Good for managed persistence |
| Host path dependent         | Docker managed               |
| Easier manual inspection    | More portable                |
| Riskier permissions         | Cleaner abstraction          |

### Investigation Questions

- For a CI pipeline's database, which would you choose, and why?
- For a developer who wants to inspect files on the host, which fits?
- What permission problems can bind mounts cause that named volumes avoid?

---

## Final Learning Outcome

You should now be able to explain, with confidence:

- **Containers are ephemeral** — their writable layer dies with `docker rm`.
- **Volumes are persistent infrastructure** — independent of any container.
- A custom image + init scripts gives every developer and CI run an
  identical, auto-seeded database.
- Named volumes are Docker-managed and portable; bind mounts give direct host
  access at the cost of portability and permission safety.

That distinction is one of the most important concepts in real DevOps work.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
| ------- | ------------ | --- |
| `bind: address already in use` on `-p 27017:27017` | Port taken (local MongoDB or old container) | Stop the other process, or map a different host port: `-p 27018:27017` and connect on `27018` |
| `docker: ... name "mongo-lab" is already in use` | Old container still exists | `docker rm -f mongo-lab` then re-run |
| `Authentication failed` in `mongosh` | Wrong creds, or missing `?authSource=admin` for root | Use the exact cheat-sheet URIs in Setup |
| `Seed complete` never appears in logs | Volume was **not** fresh — init only runs on empty `/data/db` | `docker rm -f mongo-lab; docker volume rm mongodata; docker volume create mongodata`, then re-run |
| `appuser` auth fails | Seed never ran (see above), so the user was never created | Recreate on a fresh volume so `01-seed.js` runs |
| `not authorized on otherdb` as `appuser` | **Expected** — least privilege working (Part 6) | Not an error; this is the lesson |
| Data gone after `docker rm` | No `-v` volume mounted (Parts 1–2) | Mount `-v mongodata:/data/db` (Part 3+) |
| `mongosh: command not found` | Shell not installed | Install mongosh, or use `docker exec mongo-lab mongosh ...` instead |

---

## Deliverables

Submit the following:

1. **Your `Dockerfile`** (the one you wrote on `main`).
2. **Command history** — the `docker` / `docker volume` / `mongosh` commands
   you ran for each part (paste from terminal history or a saved script).
3. **Evidence of data loss → persistence:**
   - Part 2: output showing the data is **gone** after `docker rm`.
   - Part 4: output showing the data **survived** `docker rm` with a volume.
4. **Seed proof:** the `docker logs` snippet showing `Seed complete`
   (users: 3, products: 4, orders: 3).
5. **`appuser` proof:** output of a query run as `appuser`, **and** the
   `not authorized` error when acting outside `appdb`.
6. **`docker volume inspect` output** for your volume (name, mountpoint,
   driver).
7. **Written answers** to every *Investigation Question* in Parts 1–8.

Submit as a single markdown or PDF file (commands + pasted outputs +
answers). Screenshots acceptable for terminal output.
