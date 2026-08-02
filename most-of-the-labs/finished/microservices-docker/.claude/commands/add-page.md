# Add Page

Create a new React page for: $ARGUMENTS

Read these files before generating code to match exact patterns:
- `Client/src/config/routesConfig.tsx` (RouteConfig interface, routeConfig array)
- `Client/src/pages/Layout.tsx` (layout structure)
- `Client/src/pages/DashboardPage.tsx` (page component pattern)
- `Client/src/components/ProtectedRoute.tsx` (if auth required)
- `Client/src/lib/utils.ts` (cn utility)

## Steps

### 1. Page component in `Client/src/pages/<Name>Page.tsx`
- Functional React component with TypeScript
- Use existing Atomic Design components:
  - Atoms: `Badge`, `Card`, `Heading`, `Text`, `Icon`, `LoadingSpinner`, `Link` from `@/components/Atoms/`
  - Molecules: `Hero`, `Section`, `FeatureCard` from `@/components/Molecules/`
- Use `cn()` from `@/lib/utils` for conditional class merging
- Icons from `lucide-react`
- Tailwind CSS v4 for styling
- Framer Motion for animations if appropriate
- If page needs data: use TanStack Query hooks or Redux selectors
- If page needs auth data: use `useAuth0()` from `@auth0/auth0-react` and `useAppSelector` from `@/redux/hooks`

### 2. Loader function (optional)
- Export `export const <Name>PageLoader = async () => { ... }` if the page needs data prefetching
- Return data that the page component can access

### 3. Add to route config in `Client/src/config/routesConfig.tsx`
- Import the page component
- Import an icon from `lucide-react`
- Add entry to `routeConfig` array:
  ```typescript
  {
    path: "/feature-name",
    name: "Feature Name",
    Component: FeatureNamePage,
    icon: SomeIcon,          // from lucide-react
    showInSidebar: true,     // false for sub-pages
    requireAuth: true,       // false for public pages
    requiredRole: undefined, // or "admin"
  }
  ```
- For nested pages, add as `children` array under parent route with `index: true` for default child

### 4. If the page is a sub-page of an existing route
- Add it to the parent's `children` array in routeConfig
- It will automatically appear in sidebar submenu via `getSidebarMenuItems()`
