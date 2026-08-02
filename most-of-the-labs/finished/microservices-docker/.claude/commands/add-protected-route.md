# Add Auth0-Protected Route

Add an authenticated API endpoint: $ARGUMENTS

Read these files before generating code to match exact patterns:
- `Server/src/routes/authRoutes.ts` (auth0Middleware usage)
- `Server/src/controllers/authControllers.ts` (req.auth.payload access)
- `Server/src/middleware/auth0Mdw.ts` (how auth works)
- `Server/src/models/userModel.ts` (User.findByAuth0Id static)

## Steps

### 1. Controller method
- Add method to existing controller class or create new one in `Server/src/controllers/`
- Access the authenticated user via `req.auth.payload`:
  - `req.auth.payload.sub` — Auth0 user ID
  - Use `User.findByAuth0Id(sub)` to get the user from DB
- Validate request body with Zod if needed
- Return `res.status(code).json({ success: true, data: ... })`

### 2. Zod validation (if request has a body)
- Add or update schema in `Server/src/zod/<resource>Zod.ts`

### 3. Route with auth middleware
- In the route file, apply auth middleware BEFORE the handler:
  ```
  router.post("/path", auth0Middleware, asyncHandler(controller.method.bind(controller)))
  ```
- Import `auth0Middleware` from `@/middleware/auth0Mdw`
- Import `asyncHandler` from `@/utils/errorHandler`

### 4. Register route file (if new)
- Add `app.use("/api/<resource>", routes)` in `Server/src/server.ts`

### 5. Client service (if needed)
- The auth token is already set globally on axios by `Client/src/components/AppInitializer.tsx`
- Service functions don't need to manually set Authorization headers
- Just use `api.get("/api/...")` or `api.post("/api/...", data)` from `Client/src/services/api.ts`

### 6. Update `CLAUDE.md`
- Add the endpoint to the Routes section with `(auth required)` notation
