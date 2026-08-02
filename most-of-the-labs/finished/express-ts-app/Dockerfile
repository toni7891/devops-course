# Build stage
FROM node:22-slim AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build && npm prune --omit=dev

# Runtime stage
FROM gcr.io/distroless/nodejs22-debian12

WORKDIR /app

COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist

ENV PORT=3000
EXPOSE 3000

CMD ["dist/index.js"]
