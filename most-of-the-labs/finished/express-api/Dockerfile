FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json tsconfig.json ./
RUN npm ci
COPY src ./src
RUN npm run build

FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY --from=build /app/dist ./dist

ARG COMMIT_SHA=local
ENV COMMIT_SHA=$COMMIT_SHA

EXPOSE 3000
USER node
CMD ["node", "dist/server.js"]
