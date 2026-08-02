FROM --platform=linux/amd64 node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev
COPY server.js ./

FROM --platform=linux/amd64 gcr.io/distroless/nodejs20-debian12:nonroot
WORKDIR /app
COPY --from=build --chown=nonroot:nonroot /app /app
USER nonroot
EXPOSE 3000
CMD ["server.js"]