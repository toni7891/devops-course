# express-ts-app

Express + TypeScript API with in-memory CRUD. Production runtime is a Google **distroless** Node 22 image running compiled JS with prod-only `node_modules`.

## Routes

| Method | Path         | Body            | Description    |
|--------|--------------|-----------------|----------------|
| GET    | `/health`    | —               | health check   |
| GET    | `/items`     | —               | list items     |
| GET    | `/items/:id` | —               | get one item   |
| POST   | `/items`     | `{ "name": "" }`| create item    |
| PUT    | `/items/:id` | `{ "name": "" }`| update item    |
| DELETE | `/items/:id` | —               | delete item    |

## Dev

```bash
npm install
npm run dev          # tsx watch, http://localhost:3000
```

## Build + run

```bash
npm run build        # tsc -> dist/
npm start            # node dist/index.js
```

## Docker (distroless)

```bash
docker build -t express-ts-app .
docker run --rm -p 3000:3000 express-ts-app
curl http://localhost:3000/health
curl -X POST http://localhost:3000/items -H "content-type: application/json" -d '{"name":"a"}'
curl http://localhost:3000/items
docker history express-ts-app   # final layer: gcr.io/distroless/nodejs22-debian12
```
