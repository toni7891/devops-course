# Add Express Middleware

Create Express middleware for: $ARGUMENTS

Read these files before generating code to match exact patterns:
- `Server/src/middleware/auth0Mdw.ts`
- `Server/src/utils/errorHandler.ts` (AppError class, asyncHandler)
- `Server/src/server.ts` (middleware registration order)

## Steps

### 1. Create middleware in `Server/src/middleware/<name>Mdw.ts`
- Export a middleware function: `(req: Request, res: Response, next: NextFunction) => void`
- For error cases, throw `AppError` with appropriate status code — it will be caught by the error handler
- For async operations, wrap logic in try/catch and call `next(error)` on failure
- Keep middleware focused on a single responsibility

### 2. Register in `Server/src/server.ts`
- Import the middleware
- Place it in the correct position in the middleware chain:
  - Security/auth middleware: after CORS, before routes
  - Logging/parsing middleware: after CORS, before routes
  - Route-specific middleware: in the route file, not in server.ts
- Current middleware order: cors → rateLimit → morgan → connectDB → json → urlencoded → routes → errorHandler
- **errorHandler must always be last**

### 3. If route-specific (not global)
- Don't add to server.ts middleware chain
- Instead, apply per-route in route files: `router.get("/path", myMiddleware, asyncHandler(controller.method.bind(controller)))`
- Follow the pattern in `Server/src/routes/authRoutes.ts` where `auth0Middleware` is applied per-route
