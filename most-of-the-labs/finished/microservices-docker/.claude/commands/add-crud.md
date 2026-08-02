# Add Full CRUD

Create complete CRUD (Create, Read, Update, Delete) for: $ARGUMENTS

This is a full-stack command. Read ALL reference files before generating code.

## Reference files to read first
- `Server/src/types/usersTypes.ts`
- `Server/src/models/userModel.ts`
- `Server/src/zod/usersZod.ts`
- `Server/src/controllers/usersControllers.ts`
- `Server/src/routes/userRoutes.ts`
- `Server/src/server.ts`
- `Client/src/services/api.ts`
- `Client/src/services/users.ts`
- `Client/src/config/routesConfig.tsx`

## Server Side

### 1. Types — `Server/src/types/<resource>Types.ts`
- `I<Resource>` interface with all fields
- `I<Resource>Doc extends I<Resource>, Document`
- `I<Resource>Model extends Model<I<Resource>Doc>` with static methods

### 2. Model — `Server/src/models/<resource>Model.ts`
- Mongoose schema with timestamps, field validators, unique constraints
- Static methods for common queries
- Export `mongoose.model<I<Resource>Doc, I<Resource>Model>()`

### 3. Zod — `Server/src/zod/<resource>Zod.ts`
- `create<Resource>Schema` — all required fields validated
- `update<Resource>Schema` — `.partial()` for optional updates

### 4. Controller — `Server/src/controllers/<resource>Controllers.ts`
Class with 5 methods:
- `create<Resource>` — validate with Zod, create doc, return 201
- `get<Resources>` — find all, return 200
- `get<Resource>ById` — findById, throw 404 if not found, return 200
- `update<Resource>` — validate with Zod, findByIdAndUpdate, throw 404 if not found, return 200
- `delete<Resource>` — findByIdAndDelete, throw 404 if not found, return 200

### 5. Routes — `Server/src/routes/<resource>Routes.ts`
```
POST   /            → create<Resource>
GET    /            → get<Resources>
GET    /:id         → get<Resource>ById
PATCH  /:id         → update<Resource>
DELETE /:id         → delete<Resource>
```
All wrapped with `asyncHandler(controller.method.bind(controller))`.
Add `auth0Middleware` if the resource requires authentication.

### 6. Register — `Server/src/server.ts`
- `app.use("/api/<resources>", <resource>Routes)`

## Client Side

### 7. Service — `Client/src/services/<resource>.ts`
- Functions for all 5 operations using shared `api` instance
- `return data.data` to unwrap server response

### 8. TanStack Query hooks — `Client/src/hooks/use<Resource>.ts`
- `use<Resources>()` — useQuery for list
- `use<Resource>(id)` — useQuery for single item
- `useCreate<Resource>()` — useMutation + invalidateQueries
- `useUpdate<Resource>()` — useMutation + invalidateQueries
- `useDelete<Resource>()` — useMutation + invalidateQueries

### 9. List page — `Client/src/pages/<Resources>Page.tsx`
- Display data using `@tanstack/react-table` if tabular
- Loading state with `LoadingSpinner`
- Error state handling
- Create/Edit actions

### 10. Route config — `Client/src/config/routesConfig.tsx`
- Add to `routeConfig` array with icon, sidebar visibility, auth requirements

## Final Steps
- Update `CLAUDE.md` Routes section with all new endpoints
- Verify all imports use `@/` path alias
- Response format: `{ success: true, data: ... }`
