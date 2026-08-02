# New Feature Scaffold

Create a complete full-stack MERN feature for: $ARGUMENTS

Follow the existing project patterns exactly. Read the existing files referenced below before generating code.

## Server Side

### 1. TypeScript types in `Server/src/types/<feature>Types.ts`
- `I<Feature>` interface for business logic fields
- `I<Feature>Doc extends I<Feature>, Document` for Mongoose documents
- `I<Feature>Model extends Model<I<Feature>Doc>` for static methods
- Follow pattern in `Server/src/types/usersTypes.ts`

### 2. Mongoose model in `Server/src/models/<feature>Model.ts`
- Schema with `new Schema<I<Feature>Doc>()` and proper field types
- Enable `timestamps: true`
- Add useful static methods
- Export as `mongoose.model<I<Feature>Doc, I<Feature>Model>()`
- Follow pattern in `Server/src/models/userModel.ts`

### 3. Zod validation in `Server/src/zod/<feature>Zod.ts`
- `create<Feature>Schema` with `z.object()` and field validators
- `update<Feature>Schema` using `.partial()` for optional fields
- Follow pattern in `Server/src/zod/usersZod.ts`

### 4. Class-based controller in `Server/src/controllers/<feature>Controllers.ts`
- Class with async methods for each CRUD operation
- Validate with Zod: `schema.parse(req.body)`
- Return `res.status(code).json({ success: true, data: ... })`
- Throw `AppError` for errors (import from `@/utils/errorHandler`)
- Follow pattern in `Server/src/controllers/usersControllers.ts`

### 5. Routes in `Server/src/routes/<feature>Routes.ts`
- Import `Router` from express
- Instantiate controller: `const controller = new <Feature>Controller()`
- Wrap handlers: `asyncHandler(controller.method.bind(controller))`
- Apply `auth0Middleware` on protected routes
- Follow pattern in `Server/src/routes/userRoutes.ts`

### 6. Register in `Server/src/server.ts`
- Import the routes file
- Add `app.use("/api/<feature>", <feature>Routes)` in the routes section

## Client Side

### 7. API service in `Client/src/services/<feature>.ts`
- Named async functions for each endpoint
- Use the shared axios instance: `import api from './api'`
- Return `data.data` from response
- Follow pattern in `Client/src/services/users.ts`

### 8. Page component in `Client/src/pages/<Feature>Page.tsx`
- Functional React component
- Use TanStack Query for data fetching if read-heavy
- Use existing Atomic Design components from `Client/src/components/`
- Follow pattern in `Client/src/pages/HomePage.tsx`

### 9. Add route to `Client/src/config/routesConfig.tsx`
- Add entry to `routeConfig` array with path, name, Component, icon, showInSidebar, requireAuth, requiredRole
- Import the page component and a lucide-react icon

### 10. Redux slice (if needed) in `Client/src/redux/slices/<feature>Slice.ts`
- Only if the feature needs global state management
- Use `createSlice()` with `createAsyncThunk()` for async ops
- Follow pattern in `Client/src/redux/slices/userSlice.ts`

## Final Steps
- Update `CLAUDE.md` Routes section with the new endpoints
- Verify all imports use the `@/` path alias
- Ensure the feature follows the existing response format: `{ success: true, data: ... }`