# Debug

Diagnose and troubleshoot: $ARGUMENTS

If no specific issue is given, run a full health check of the project.

## Full Health Check Sequence

### 1. Docker Status
- Run `docker compose ps` to check container status
- Run `docker compose logs --tail=50` to check recent logs
- Verify both server and client containers are running and healthy

### 2. Database Connection
- Check `Server/.env` has a valid `MONGO_URI`
- Hit `GET /danger/db-health` endpoint (dev only) to verify DB connection
- Check if MongoDB Atlas is reachable: look for connection errors in server logs

### 3. API Health
- Hit `GET /health` endpoint to verify Express is running
- Check server logs for startup errors
- Verify CORS is configured correctly (CLIENT_URL in Server/.env matches Client URL)

### 4. Auth0 Configuration
- Verify `Server/.env` has AUTH0_DOMAIN and AUTH0_AUDIENCE
- Verify `Client/.env` has VITE_AUTH0_DOMAIN, VITE_AUTH0_CLIENT_ID, VITE_AUTH0_AUDIENCE
- Check if Auth0 domain values match between Server and Client
- Hit `GET /api/auth/validate` with a token to test JWT validation

### 5. Vite Proxy
- Check `Client/vite.config.ts` proxy settings
- Verify VITE_PROXY_TARGET points to correct server URL
- Check client logs for proxy errors (502, ECONNREFUSED)

### 6. Environment Variables
- Compare `Server/.env` against `Server/.env.example` for missing vars
- Compare `Client/.env` against `Client/.env.example` for missing vars
- Check for empty or placeholder values

### 7. Dependencies
- Check if `node_modules` exist in Server/ and Client/
- Look for version conflicts in package-lock.json
- Run `npm ls` in both directories to check for peer dependency issues

### 8. TypeScript
- Run `npx tsc --noEmit` in Server/ to check for type errors
- Run `npx tsc --noEmit` in Client/ to check for type errors

### 9. Lint
- Run `npm run lint` in Client/ to check ESLint errors

## Common Issues

### "Cannot connect to server" from Client
- Docker: Check if server container is running (`docker compose ps`)
- Proxy: Check Vite proxy config, server should be reachable at `http://server:3000` inside Docker
- CORS: Check CLIENT_URL in Server/.env

### "Unauthorized" errors
- Check Auth0 env vars match between Server and Client
- Verify Auth0 audience is the same in both
- Check if token is being set on axios: look at AppInitializer.tsx flow

### "MongoDB connection failed"
- Check MONGO_URI in Server/.env
- Verify IP whitelist on MongoDB Atlas
- Check network connectivity from Docker container
