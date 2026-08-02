FROM node:24-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci


FROM gcr.io/distroless/nodejs24

WORKDIR /app

COPY --from=build /app/node_modules ./node_modules

COPY src src

ENV PORT=3000

CMD ["src/server.js"]