# `company-api`

A small NestJS service used as the subject of a DevOps release-engineering lab.

**If you are a student:** read [LAB.md](LAB.md). That is your assignment.

---

## Endpoints

- `GET /health` — `{ status, uptime }`
- `GET /version` — `{ version, commit, buildDate }` (read from `APP_VERSION`, `COMMIT_SHA`, `BUILD_DATE` env vars)
- `GET /users` — CRUD scaffold

## Local dev

```bash
npm install
npm run start:dev
curl localhost:3000/health
```

## Stack

NestJS 10 · Node 20 · TypeScript 5.
