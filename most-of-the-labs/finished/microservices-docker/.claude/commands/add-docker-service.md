# Add Docker Service

Add a new Docker service for: $ARGUMENTS

Read these files before generating code to match exact patterns:
- `docker-compose.yml` (root, uses include: directive)
- `Server/compose.yml` (service definition pattern)
- `Server/Dockerfile` (multi-stage build pattern)
- `Client/compose.yml` (watch config pattern)

## Steps

### 1. Create service directory
- Create `<ServiceName>/` at project root (matching Server/, Client/ convention)
- Initialize with `package.json` if Node.js service, or appropriate config

### 2. Create Dockerfile — `<ServiceName>/Dockerfile`
Follow the multi-stage pattern:
```dockerfile
# Development stage
FROM node:22-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

# Build stage
FROM development AS build
RUN npm run build

# Production stage
FROM node:22-alpine AS production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/package*.json ./
RUN npm ci --only=production
CMD ["npm", "start"]
```

### 3. Create compose.yml — `<ServiceName>/compose.yml`
```yaml
services:
  <service-name>:
    container_name: <service-name>
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    ports:
      - "<port>:<port>"
    env_file:
      - .env
    volumes:
      - <service>_node_modules:/app/node_modules
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: ./package.json
        - action: rebuild
          path: ./package-lock.json
    networks:
      - mern-network

volumes:
  <service>_node_modules:

networks:
  mern-network:
    external: true
```

### 4. Update root `docker-compose.yml`
- Add `- path: ./<ServiceName>/compose.yml` to the `include:` list

### 5. Update boot script (optional)
- If the service needs customizable container name/port, add prompts in `scripts/boot.js`
- Follow existing pattern for Server/Client customization

### 6. Add .env.example
- Create `<ServiceName>/.env.example` with required environment variables
- Update `scripts/boot.js` to copy this to `.env` during boot (follow existing pattern)
