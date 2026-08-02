FROM node:24-alpine as build

WORKDIR /app
COPY package*.json .
RUN npm ci

COPY src/ src/ /app/


FROM gcr.io/distroless/nodejs24

WORKDIR /app

COPY --from=build /app/node_modules ./node_modules

COPY --from=build /app/dist ./dist

ENV PORT=3000

CMD ["src/server.js"]