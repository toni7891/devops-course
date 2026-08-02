# express-app

Production-like Express API. JS ESM, in-memory store, no auth.

## Stack

- Express 4
- helmet, cors, compression, express-rate-limit
- pino + pino-http logging
- zod validation
- jest + supertest

## Layout

```
src/
  app.js              # express app factory
  server.js           # bootstrap + graceful shutdown
  config/             # env, logger
  errors/             # HttpError
  middleware/         # validate, errorHandler
  routes/             # health
  modules/users/      # routes -> controller -> service -> store
tests/                # supertest integration
```

## Run

```bash
cp .env.example .env
npm install
npm run dev
```

## Endpoints

- `GET  /livez`, `GET /readyz`
- `GET  /api/users`
- `POST /api/users`            `{ name, email }`
- `GET  /api/users/:id`
- `PATCH /api/users/:id`       partial `{ name?, email? }`
- `DELETE /api/users/:id`

## Test

```bash
npm test
```
