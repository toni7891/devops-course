# Topic 1 — Why a Cloud Database

**Time:** 09:30–10:00 (30 min)

---

## Objectives

- Explain the limitations of in-memory and local storage
- Define what a cloud database is and why it is used
- Introduce MongoDB Atlas as the tool for today

---

## Topics

### 1. The Problem with What We Have

Our Day 2–3 API stores tasks in a Python list:

```python
tasks = []
```

| Problem | What happens |
|---------|-------------|
| Server restarts | All data is lost |
| Two servers running | Each has its own list — they disagree |
| Another developer connects | They see empty data |
| The machine crashes | Everything is gone |

This is fine for learning — not fine for production.

### 2. Local Database — One Step Better, Still Not Enough

A local SQLite or file-based DB solves restarts, but:
- Tied to one machine
- Cannot be accessed from other services or servers
- Hard to scale
- Hard to back up

### 3. Cloud Database — What Real Systems Use

A cloud database is a database server running on infrastructure you do not manage:

```
Your API server  →  network  →  Cloud DB (MongoDB Atlas)
                                     ↑
                               Managed, backed up,
                               accessible from anywhere
```

Benefits:
- Data survives restarts and deploys
- Multiple servers share the same data
- Managed backups, monitoring, scaling
- Free tier available for development

### 4. Why MongoDB Atlas Today

- Free tier is genuinely free (no credit card for M0 cluster)
- Simple setup — ready in under 10 minutes
- GUI (Atlas UI) lets students see their data visually
- PyMongo is the simplest Python driver available
- Document model (JSON-like) matches what we already return from our API

---

## Discussion

Ask the class:

1. What happens to your tasks right now when you restart the Flask server?
2. What if we deployed our API to two machines — which tasks list would clients see?
3. Where does Google store your Gmail messages? Is it on your laptop?

---

## Key Vocabulary

| Term | Meaning |
|------|---------|
| Cluster | A group of servers running the database |
| Collection | MongoDB's equivalent of a database table |
| Document | MongoDB's equivalent of a row (stored as BSON/JSON) |
| Connection string | The URL used to connect to the database |
| Atlas | MongoDB's managed cloud database service |
