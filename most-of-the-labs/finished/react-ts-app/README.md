# react-ts-app

React + TypeScript + Vite SPA. Production runtime is a Google **distroless** Node 22 image serving the built `dist/` via a zero-dependency static server (`server.mjs`) with SPA fallback.

## Dev

```bash
npm install
npm run dev          # http://localhost:5173
```

## Build + local serve

```bash
npm run build        # outputs dist/
npm run serve        # node server.mjs -> http://localhost:8080
```

## Docker (distroless)

```bash
docker build -t react-ts-app .
docker run --rm -p 8080:8080 react-ts-app
# http://localhost:8080
docker history react-ts-app   # final layer: gcr.io/distroless/nodejs22-debian12
```
