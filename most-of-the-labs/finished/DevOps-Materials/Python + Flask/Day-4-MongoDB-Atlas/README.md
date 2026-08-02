# Day 4 — Cloud Database with MongoDB Atlas

## Goal

Replace the in-memory store with a real cloud database. Every task is now persisted in MongoDB Atlas — surviving restarts, accessible from anywhere.

> "Until now everything was local — now we work like a real system, with a cloud database"

---

## Final Project Layer

**Task Manager API v3** — PyMongo replaces the in-memory list. Services are the only layer that touch the database. Routes stay identical to Day 3.

---

## Schedule

| Time | Topic | Folder |
|------|-------|--------|
| 09:30–10:00 | Why a Cloud Database | `1-Why-Cloud-DB/` |
| 10:00–11:00 | MongoDB Atlas Setup (live) | `2-Atlas-Setup/` |
| 11:00–12:00 | Connecting with PyMongo | `3-PyMongo-Connect/` |
| 12:00–12:30 | Common Connection Problems | `4-Connection-Problems/` |
| 12:30–13:30 | Lunch | — |
| 13:30–14:30 | MongoDB CRUD Outside Flask | `5-Mongo-CRUD/` |
| 14:30–15:30 | Connect Mongo to the Project | `6-Project-Refactor/` |
| 15:30–16:30 | In-Class Final Exercise | `6-Project-Refactor/` (extended) |
| Evening | Production Mongo Integration | `7-Evening-Assignment/` |

---

## By End of Day 4, Students Will:

- Explain why cloud databases are used in production systems
- Create and configure a MongoDB Atlas cluster from scratch
- Connect a Python application to Atlas using PyMongo
- Diagnose the three most common Atlas connection failures
- Perform full CRUD operations against a MongoDB collection
- Handle `ObjectId` correctly (store as `ObjectId`, return as `string`)
- Replace an in-memory store with MongoDB without changing routes
- Read configuration from environment variables (no hardcoded secrets)
