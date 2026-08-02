# CI Lab API 🚀

A production-like Node.js + TypeScript REST API used as the base for a CI/CD lab with GitHub Actions.

## Stack

- **Runtime:** Node.js 18+
- **Language:** TypeScript
- **Framework:** Express
- **Testing:** Jest + Supertest
- **Logging:** Winston
- **Linting:** ESLint + TypeScript plugin

## Project Structure

```
ci-lab/
├── src/
│   ├── config/         # App configuration (env vars)
│   ├── middleware/     # Express middleware (logging, errors, 404)
│   ├── routes/         # Route handlers
│   ├── utils/          # Shared utilities (logger)
│   ├── app.ts          # Express app setup
│   └── index.ts        # Server entry point (with graceful shutdown)
├── test/               # Jest + Supertest tests
├── .env.example        # Environment variable template
├── jest.config.js
├── tsconfig.json
└── .eslintrc.js
```

## Getting Started

```bash
# Install dependencies
npm install

# Copy env file
cp .env.example .env

# Run in dev mode
npm run dev

# Build for production
npm run build
npm start
```

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Run with ts-node (development) |
| `npm run build` | Compile TypeScript → dist/ |
| `npm start` | Run compiled output |
| `npm test` | Run tests with coverage |
| `npm run test:ci` | Run tests with JUnit reporter (for CI) |
| `npm run lint` | Check linting |
| `npm run typecheck` | TypeScript type check only |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check with version + uptime |
| GET | `/api/items` | List all items |
| GET | `/api/items/:id` | Get item by ID |
| POST | `/api/items` | Create new item |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NODE_ENV` | `development` | Environment |
| `PORT` | `3000` | Server port |
| `LOG_LEVEL` | `info` | Winston log level |
| `APP_VERSION` | `1.0.0` | App version (injected by CI) |
