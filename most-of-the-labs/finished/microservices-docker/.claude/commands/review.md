# Code Review

Review code for: $ARGUMENTS

If no specific files are given, review all uncommitted changes by running `git diff` and `git diff --cached`.

Read `CLAUDE.md` and `docs/DESIGN_SYSTEM.md` before reviewing to understand project conventions.

## Review Checklist

### Server Architecture & Patterns
- [ ] Controllers use class-based pattern (not standalone functions)
- [ ] Controller methods are bound via `.bind(controller)` in route files
- [ ] Routes wrap handlers with `asyncHandler()` from `@/utils/errorHandler`
- [ ] Protected routes apply `auth0Middleware` before the handler
- [ ] Request bodies are validated with Zod schemas (not manual checks)
- [ ] Errors use `AppError` class with proper status codes (not raw `Error` or `res.status().json()`)
- [ ] Response format is `{ success: true, data: ... }` or `{ success: true, message: "..." }`
- [ ] New routes are registered in `Server/src/server.ts`

### TypeScript
- [ ] All imports use `@/` path alias (not relative `../` paths)
- [ ] Interfaces are defined in `Server/src/types/` or `Client/src/types/`
- [ ] No `any` types — use proper typing or `unknown`
- [ ] Mongoose models have `I*Doc` and `I*Model` interfaces in types file

### Client Architecture & Patterns
- [ ] Components follow Atomic Design hierarchy (Atoms/Molecules/Organisms)
- [ ] Components accept `className?: string` prop and use `cn()` from `@/lib/utils`
- [ ] Component variants use CVA (`class-variance-authority`)
- [ ] Icons come from `lucide-react` (not other icon libraries)
- [ ] Animations use Framer Motion (`motion` components)
- [ ] Server data fetching uses TanStack Query (not useEffect + useState)
- [ ] Global app state (user, auth) uses Redux Toolkit
- [ ] New pages are added to `routeConfig` array in `Client/src/config/routesConfig.tsx`
- [ ] API service functions return `data.data` to unwrap the server response

### Styling (from DESIGN_SYSTEM.md)
- [ ] Uses blue theme colors for primary actions
- [ ] Consistent border radius (`rounded-lg` for cards, `rounded-xl` for containers)
- [ ] Interactive elements have transitions (`transition-colors duration-200`)
- [ ] Hover and focus states on buttons, links, and cards
- [ ] Mobile-first responsive design (start with mobile, add `sm:`, `md:`, `lg:` breakpoints)
- [ ] Uses Tailwind CSS v4 utility classes
- [ ] Uses `tailwind-merge` compatible patterns via `cn()`

### Security
- [ ] No secrets, API keys, or credentials in source code
- [ ] Auth-required endpoints have `auth0Middleware` applied
- [ ] User input is validated with Zod before processing
- [ ] No `dangerouslySetInnerHTML` without sanitization
- [ ] Environment variables accessed via `process.env` (server) or `import.meta.env` (client)

### Documentation
- [ ] New API endpoints are documented in `CLAUDE.md` Routes section
- [ ] New features follow the patterns described in `CLAUDE.md`

## Output Format

For each issue found, report:

1. **File and line** — exact location
2. **Issue** — what's wrong
3. **Fix** — what should be changed
4. **Severity**:
   - **error** — breaks project conventions or has a bug
   - **warning** — inconsistency with patterns but functionally correct
   - **suggestion** — optional improvement

Group issues by file. If no issues are found, confirm the code follows all conventions.
