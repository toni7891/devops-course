# Docker Operations

Perform Docker operation: $ARGUMENTS

Determine which operation the user needs from the arguments and execute it.

## Available Operations

### Status & Inspection
- **status** / **ps**: Run `npm run docker:ps` to show container status
- **stats**: Run `npm run docker:stats` for CPU/memory usage
- **health**: Run `npm run docker:ps`, then `curl http://localhost:3000/health` and `curl http://localhost:3000/danger/db-health`

### Logs
- **logs**: Run `npm run logs` (all services)
- **logs server**: Run `npm run docker:logs:server`
- **logs client**: Run `npm run docker:logs:client`

### Lifecycle
- **start**: Run `npm run dev` (starts with `docker compose watch` for live sync)
- **start background** / **start bg**: Run `npm run dev:detached`
- **stop**: Run `npm run stop`
- **restart**: Run `npm run stop && npm run dev`
- **rebuild**: Run `npm run docker:rebuild` (stops, removes volumes, rebuilds, starts)

### Shell Access
- **shell server**: Run `npm run docker:shell:server`
- **shell client**: Run `npm run docker:shell:client`

### Cleanup
- **clean**: Run `npm run reset` (stops containers and deletes volumes)

## Troubleshooting

If the user describes a problem instead of a specific operation, diagnose it:

### Containers won't start
1. Run `npm run docker:ps` to check status
2. Run `npm run logs` to check for errors (look at last 50 lines)
3. Check if Docker Desktop is running
4. Check if ports 3000 and 5173 are free
5. Try a clean rebuild: `npm run docker:rebuild`

### Hot reload not working
1. Verify the user started with `npm run dev` (not `npm run dev:detached`)
2. `docker compose watch` only syncs changes in `src/` directories
3. Changes to `package.json` trigger a full rebuild (expected delay)
4. Check logs for errors: `npm run docker:logs:server` and `npm run docker:logs:client`

### Cannot connect to MongoDB Atlas
1. Check `Server/.env` has a valid `MONGO_URI`
2. Hit `curl http://localhost:3000/danger/db-health` to check connectivity
3. Verify IP whitelist on MongoDB Atlas includes the current IP (or `0.0.0.0/0` for dev)
4. Check server logs: `npm run docker:logs:server`

### Port conflicts
1. Identify what's using the port:
   - Windows: `netstat -ano | findstr :<port>`
   - Linux/Mac: `lsof -i :<port>`
2. Either kill the conflicting process or change ports in `Server/.env` / `Client/.env`
3. Rebuild: `npm run docker:rebuild`

### API requests failing from client
1. Check that the Vite proxy is working — client proxies `/api/*` to `http://server:3000` inside Docker
2. Check `Client/vite.config.ts` proxy settings
3. Verify server is running: `curl http://localhost:3000/health`
4. Check server logs for errors: `npm run docker:logs:server`

### "Module not found" errors
1. This usually means `node_modules` volume is stale
2. Run `npm run docker:rebuild` to recreate volumes and reinstall dependencies
