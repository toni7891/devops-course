# Microservices Lab — Starter

This is the **starter** for a hands-on lab on dockerizing a microservices app.

You're given a working application — two backend services, an Nginx config for a load balancer, and a static frontend — but **no Docker files**. Your task is to dockerize it step by step.

➡️ **[Start the lab](./lab/README.md)**

The complete reference implementation lives on the `solution` branch:

```bash
git checkout solution                          # browse the full solution
git checkout solution -- path/to/file          # grab one file
git diff solution -- path/to/file              # compare yours to the solution
```

## The app

- **`services/users-service/`** — Express + MongoDB. Manages users (name, email).
- **`services/products-service/`** — Express + MongoDB. Manages products with atomic stock decrement (`POST /products/:id/buy`).
- **`lb/nginx.conf`** — API gateway config: routes `/users/*` and `/products/*` to the right service.
- **`frontend/`** — static HTML/CSS/JS app that calls `/api/users` and `/api/products`.

## Layout

```
.
├── lab/                         ← lab instructions, one file per step
├── frontend/
│   ├── nginx.conf
│   └── public/index.html
├── lb/
│   └── nginx.conf
└── services/
    ├── users-service/{server.js, package.json}
    └── products-service/{server.js, package.json}
```
