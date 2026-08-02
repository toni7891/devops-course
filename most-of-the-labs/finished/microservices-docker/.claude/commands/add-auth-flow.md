# Add Role-Based Auth Flow

Add role-based access control for: $ARGUMENTS

Read these files before generating code to match exact patterns:
- `Server/src/middleware/auth0Mdw.ts` (auth middleware)
- `Server/src/controllers/authControllers.ts` (req.auth.payload usage)
- `Server/src/models/userModel.ts` (user role field: enum ['admin', 'user'])
- `Client/src/components/ProtectedRoute.tsx` (requiredRole check)
- `Client/src/config/routesConfig.tsx` (requiredRole in route config)

## Server Side

### 1. Role middleware in `Server/src/middleware/roleMdw.ts` (if doesn't exist)
Create a role-checking middleware:
```typescript
import { Request, Response, NextFunction } from "express";
import { AppError } from "@/utils/errorHandler";
import User from "@/models/userModel";

export const requireRole = (...roles: string[]) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const sub = req.auth?.payload?.sub;
    if (!sub) throw new AppError("Unauthorized", 401);

    const user = await User.findByAuth0Id(sub);
    if (!user) throw new AppError("User not found", 404);
    if (!roles.includes(user.role)) throw new AppError("Forbidden", 403);

    next();
  };
};
```

### 2. Apply to routes
- Chain middlewares: `auth0Middleware, requireRole("admin"), asyncHandler(...)`
- auth0Middleware validates the JWT token
- requireRole checks the user's role in the database

### 3. Add new role to user model (if needed)
- Update the role enum in `Server/src/models/userModel.ts`: `enum: ['admin', 'user', 'newRole']`
- Update `Server/src/types/usersTypes.ts` role type

## Client Side

### 4. Route config with requiredRole
- In `Client/src/config/routesConfig.tsx`, set `requiredRole` on protected routes:
  ```typescript
  {
    path: "/admin-panel",
    name: "Admin Panel",
    Component: AdminPanelPage,
    requireAuth: true,
    requiredRole: "admin",
    showInSidebar: true,
  }
  ```

### 5. ProtectedRoute handles it automatically
- `Client/src/components/ProtectedRoute.tsx` already checks `requiredRole` against `user.role` from Redux
- `getSidebarMenuItems()` in routesConfig already filters sidebar items by role
- No additional client code needed — just set the config correctly

### 6. Conditional UI rendering (if needed)
```typescript
const { user } = useAppSelector((state) => state.user);
if (user?.role === "admin") { /* show admin controls */ }
```
