# Todo App — Base (No Docker)

Simple full-stack todo app, runs directly on your machine. No Docker, no database — todos live in memory and reset on restart.

This is the **starting point**. Compare it to `../app-docker/` to see exactly what Docker adds.

## Features

- Express backend with REST API
- React + Vite frontend with hot reload
- In-memory storage (no DB)
- Vite proxy avoids CORS

## Project Structure

```
app-base/
├── backend/
│   ├── package.json
│   └── server.js          # Express app, port 3000
└── frontend/
    ├── package.json
    ├── vite.config.js     # proxy /api -> localhost:3000
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx        # todo UI
        └── App.css
```

## Quick Start

You need **two terminals**.

**Terminal 1 — backend:**
```bash
cd backend
npm install
npm run dev
```

**Terminal 2 — frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## API

| Method | Path             | Body            |
|--------|------------------|-----------------|
| GET    | `/api/todos`     | —               |
| POST   | `/api/todos`     | `{ "text": "" }`|
| DELETE | `/api/todos/:id` | —               |

Test directly:
```bash
curl http://localhost:3000/api/todos
```

## How the Proxy Works

Frontend code calls `/api/todos` (relative path). Vite dev server forwards `/api/*` to `http://localhost:3000`. No CORS, no env vars.

## Next Step

See `../app-docker/` — same app, containerized with Docker Compose.
