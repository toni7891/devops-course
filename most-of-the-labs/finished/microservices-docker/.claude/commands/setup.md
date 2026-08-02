# Project Setup from Template

Customize this MERN template for a new project: $ARGUMENTS

Read `docs/TEMPLATE_GUIDE.md` for full context before starting.

## Steps

### 1. Update project identity
- Update `name` in root `package.json`
- Update `name` in `Server/package.json`
- Update `name` in `Client/package.json`
- Update `<title>` in `Client/index.html`
- Update app name in `Client/src/components/Organisms/Sidebar.tsx` and `Client/src/components/Organisms/Footer.tsx`

### 2. Run boot script
- Run `npm run boot` to configure Docker container names, image names, ports, and network name
- This also copies `.env.example` to `.env` in both Server/ and Client/

### 3. Configure environment variables
- Edit `Server/.env`:
  - `MONGO_URI` — MongoDB Atlas connection string
  - `AUTH0_DOMAIN` — Auth0 tenant domain
  - `AUTH0_AUDIENCE` — Auth0 API identifier
  - `CLIENT_URL` — Frontend URL (default: http://localhost:5173)
- Edit `Client/.env`:
  - `VITE_AUTH0_DOMAIN` — Auth0 tenant domain (must match server)
  - `VITE_AUTH0_CLIENT_ID` — Auth0 application client ID
  - `VITE_AUTH0_AUDIENCE` — Auth0 API identifier (must match server)

### 4. Verify Auth0 configuration
- Auth0 Application settings:
  - Allowed Callback URLs: `http://localhost:5173`
  - Allowed Logout URLs: `http://localhost:5173`
  - Allowed Web Origins: `http://localhost:5173`
- Auth0 API settings:
  - Identifier must match `AUTH0_AUDIENCE` / `VITE_AUTH0_AUDIENCE`

### 5. Customize branding
- Read `docs/DESIGN_SYSTEM.md` for the current design system
- Update color scheme: modify CSS variables in `Client/src/index.css`
- Replace favicon in `Client/public/`
- Update logo references in components if applicable

### 6. Clean up template files
- Update root `README.md` for the new project
- Update `CLAUDE.md` project description and any project-specific details
- Optionally update or remove docs that are template-specific

### 7. Test the setup
- Run `npm run dev` to start Docker development environment
- Verify http://localhost:5173 loads the client
- Verify http://localhost:3000/health returns `{ success: true }`
- Test Auth0 login flow if credentials are configured
- Check `npm run docker:logs:server` for any errors

### 8. Remove template sample code (optional)
- If the project doesn't need the Users CRUD example:
  - Remove user-related controllers, routes, services (keep the model if Auth0 flow needs it)
  - Clean up routesConfig to remove sample pages
  - Update `CLAUDE.md` Routes section accordingly
