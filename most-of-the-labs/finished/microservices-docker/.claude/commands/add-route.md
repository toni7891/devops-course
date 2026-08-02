# Add API Route

Add REST endpoint: $ARGUMENTS

Follow the existing project patterns exactly. Read the referenced files before generating code.

## Steps

### 1. Determine scope
- If a controller class already exists for this resource, add a method to it
- If not, create a new controller class in `Server/src/controllers/`

### 2. Zod validation schema
- Add or update schema in `Server/src/zod/<resource>Zod.ts`
- Use `z.object()` with appropriate field validators
- Follow pattern in `Server/src/zod/usersZod.ts`

### 3. Controller method
- Add async method to the controller class
- Validate request body with Zod: `schema.parse(req.body)`
- Return `res.status(code).json({ success: true, data: ... })` or `{ success: true, message: "..." }`
- Throw `AppError` for errors
- Follow pattern in `Server/src/controllers/usersControllers.ts`

### 4. Route registration
- Add route in `Server/src/routes/<resource>Routes.ts`
- Wrap with `asyncHandler(controller.method.bind(controller))`
- Add `auth0Middleware` before the handler if the route requires authentication
- If this is a new route file, register it in `Server/src/server.ts`: `app.use("/api/<resource>", routes)`
- Follow pattern in `Server/src/routes/userRoutes.ts`

### 5. Client service (if needed)
- Add function in `Client/src/services/<resource>.ts`
- Use the shared axios instance from `Client/src/services/api.ts`
- Follow pattern in `Client/src/services/users.ts`

### 6. Documentation
- Update `CLAUDE.md` Routes section with the new endpoint: method, path, description, auth requirement
