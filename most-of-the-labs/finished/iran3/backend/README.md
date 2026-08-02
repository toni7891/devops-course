# ShopFlow Backend

NestJS + TypeScript REST API backed by PostgreSQL.

## Requirements

- Node.js 20+
- PostgreSQL 16+

## Setup

```bash
npm install
```

Create a `.env` file in the `backend/` directory:

```env
NODE_ENV=development
PORT=3000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=company
DB_USER=admin
DB_PASSWORD=admin123
```

## Running

```bash
# Development (watch mode)
npm run start:dev

# Production
npm run build
npm run start
```

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/health` | Liveness check |
| GET | `/ready` | Readiness check |
| GET | `/products` | Get all products |
| GET | `/products/:id` | Get single product |
| PATCH | `/products/:id/stock` | Update stock — body: `{ "delta": -1 }` |

## Running with Docker (DB only)

```bash
docker run -d \
  --name postgres-db \
  --network postgres-network \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin123 \
  -e POSTGRES_DB=company \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:17
```

Then run the backend locally with `npm run start:dev`.
