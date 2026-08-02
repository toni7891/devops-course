# deps stage
FROM node:20-alpine AS deps

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

RUN npm ci

COPY . .

#builder stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/package.json ./
COPY tsconfig.json ./
COPY src ./src
COPY tsconfig.build.json ./
COPY nest-cli.json ./

RUN npm run build && npm prune --omit=dev

#production stage
FROM gcr.io/distroless/nodejs20-debian12:nonroot

WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

ARG VERSION=dev
ARG COMMIT_SHA=unknown
ARG BUILD_DATE=unknown

ENV APP_VERSION=$VERSION
ENV COMMIT_SHA=$COMMIT_SHA
ENV BUILD_DATE=$BUILD_DATE

LABEL org.opencontainers.image.version=$VERSION \
    org.opencontainers.image.revision=$COMMIT_SHA \
    org.opencontainers.image.created=$BUILD_DATE

USER nonroot

EXPOSE 3000

CMD ["dist/main.js"]



