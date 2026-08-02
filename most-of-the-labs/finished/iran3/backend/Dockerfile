# --- Stage 1: Build ---
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY nest-cli.json tsconfig.json ./
COPY src/ ./src/

RUN npm run build

# --- Stage 2: Prod --- (distroless)
FROM gcr.io/distroless/nodejs20-debian12 AS production

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

ENV DB_HOST=shopflow-postgres
ENV DB_PORT=5432
ENV DB_NAME=company
ENV DB_USER=admin
ENV DB_PASSWORD=admin123
ENV NODE_ENV=development
ENV PORT=3001

EXPOSE 3001

CMD ["dist/main.js"]
