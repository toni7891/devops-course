# MERN Order Management App

Simple order management system built for Kubernetes/EKS deployment practice.

## Architecture

```
Browser → nginx:80 → /api/*  → backend:3000 → MongoDB
                   → /*      → React static build
```

## Services

| Service  | Image base      | Port |
|----------|-----------------|------|
| backend  | node:20-alpine  | 3000 |
| frontend | nginx:alpine    | 80   |
| mongodb  | mongo:7.0       | 27017|

## Quick Start (Docker Compose)

```bash
docker compose up --build
```

Open http://localhost — register an account and start managing orders.

## Local Development (without Docker)

```bash
# Terminal 1 — MongoDB
docker run -d -p 27017:27017 mongo:7.0

# Terminal 2 — Backend
cd backend && npm install && npm run dev

# Terminal 3 — Frontend
cd frontend && npm install && npm run dev
# Open http://localhost:5173
```

## Environment Variables

| Variable   | Required | Default | Description                |
|------------|----------|---------|----------------------------|
| MONGO_URI  | Yes      | —       | MongoDB connection string   |
| JWT_SECRET | Yes      | —       | Secret for signing JWTs     |
| PORT       | No       | 3000    | Backend listen port         |

## API Endpoints

| Method | Path                  | Auth | Description         |
|--------|-----------------------|------|---------------------|
| POST   | /api/auth/register    | No   | Register new user   |
| POST   | /api/auth/login       | No   | Login, get JWT      |
| GET    | /api/orders           | Yes  | List user's orders  |
| POST   | /api/orders           | Yes  | Create order        |
| PUT    | /api/orders/:id       | Yes  | Update order        |
| DELETE | /api/orders/:id       | Yes  | Delete order        |

Auth header: `Authorization: Bearer <token>`

## Kubernetes Deployment Notes

1. Push images to ECR (or any registry)
2. Create secrets:
   ```bash
   kubectl create secret generic backend-secrets \
     --from-literal=MONGO_URI=<your-mongo-uri> \
     --from-literal=JWT_SECRET=<your-secret>
   ```
3. Deploy backend as a Deployment + ClusterIP Service named `backend`
4. Deploy frontend as a Deployment + LoadBalancer Service (or Ingress)
5. The name `backend` in `nginx.conf` resolves via K8s DNS to the ClusterIP Service

## Health Check

```
GET /health → {"status":"ok"}
```

Used for Kubernetes liveness and readiness probes.
