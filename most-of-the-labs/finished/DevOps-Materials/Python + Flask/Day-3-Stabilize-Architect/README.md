# Day 3 — Stabilize, Investigate, Architect

## Goal

Harden the Task Manager API: real validation, professional error handling, and a clean architecture that is ready to swap in a database on Day 4.

> "Today you work like developers — not like students"

---

## Final Project Layer

**Task Manager API v2** — stabilized, architecturally layered, DB-swap-ready.

---

## Day Structure

| Part | Theme | Time |
|------|-------|------|
| Part 1 | Fix & Improve (Stabilize) | 10:00–12:30 |
| Part 2 | Research (Error Handling) | 13:30–14:45 |
| Part 3 | DB Prep (Architect) | 14:45–16:30 |

---

## Schedule

| Time | Topic | Folder |
|------|-------|--------|
| 09:30–10:00 | Day Opening & Goal Setting | `1-Opening/` |
| 10:00–12:30 | Stabilize Your API | `2-Stabilize-API/` |
| 12:30–13:30 | Lunch | — |
| 13:30–14:45 | Flask Error Handling Deep Dive | `3-Error-Handling/` |
| 14:45–16:30 | Think Like a Database (DB Prep Refactor) | `4-DB-Prep/` |
| Evening | Pre-Database Refactor Assignment | `5-Evening-Assignment/` |

---

## By End of Day 3, Students Will:

- Produce a stable, edge-case-proof CRUD API
- Apply real field validation (length, type checks)
- Use string-coded error responses (`"code": "TASK_NOT_FOUND"`)
- Register global Flask error handlers
- Understand why global handlers beat per-route try/except for HTTP errors
- Define a Task class and isolate it in a `models/` layer
- Fully separate HTTP, logic, and data layers
- Write code that can be migrated to SQLAlchemy with minimal changes
