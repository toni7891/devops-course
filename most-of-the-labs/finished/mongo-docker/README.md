# MongoDB + Docker Named Volumes Lab

A hands-on DevOps lab. You containerize MongoDB, feel the pain of ephemeral
containers, then fix it with Docker **named volumes** — and extend the setup
with a custom Dockerfile, init scripts, and bind mounts.

## The Story

A backend team builds an internal app. Developers each run MongoDB on their
laptops. The DevOps team standardizes the environment with Docker so every
developer and CI pipeline uses the **exact same** MongoDB setup.

It works — until someone removes the container and **all the data is gone**.
Your job: make MongoDB data survive the container lifecycle.

## What You'll Learn

- Containers are ephemeral; their writable layer dies with them
- Named volumes are independent, persistent infrastructure
- Where Docker stores volume data
- Building a custom MongoDB image with a Dockerfile
- Auto-seeding a database with init scripts
- Named volumes vs bind mounts — trade-offs

## Prerequisites

- Docker installed and running
- `mongosh` (MongoDB Shell) — or MongoDB Compass
- Basic terminal/CLI comfort

## How to Use This Repo

| Branch     | Purpose                                                        |
| ---------- | -------------------------------------------------------------- |
| `main`     | **Skeleton.** Stub files with TODOs. You do the work here.     |
| `solution` | **Reference.** Working Dockerfile + seed. Check when stuck.    |

```bash
git checkout main        # your working branch (default)
git checkout solution    # peek at the reference solution
```

## Start

Open [LAB.md](LAB.md) and work through Parts 1–8 in order.
