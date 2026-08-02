# Topic 1 — Day 1 Recap & Client vs Server

**Time:** 09:30–10:15 (45 min)

---

## Objectives

- Solidify understanding of the HTTP request/response lifecycle
- Identify that Day 1 code was always the **client** side
- Frame today's goal: we will build the **server** side

---

## Topics

### 1. The Full Lifecycle

```
Client → HTTP Request → Server → Business Logic → HTTP Response (JSON)
```

Every step has a role:
- **Client** — makes the request (our Day 1 code, browsers, curl)
- **HTTP** — the transport protocol (method, headers, body)
- **Server** — receives, routes, processes
- **Response** — always JSON in our APIs

### 2. Looking at Day 1 Code

Open `Day-1-API-Foundations/7-Evening-Assignment/main.py`.

Ask the class:
- Who is making the HTTP call here?
- Where is the server in this code?
- What would it look like if **we** were the server?

### 3. The Gap We Are Filling Today

| Day 1 | Day 2 |
|-------|-------|
| We call external APIs | We build our own API |
| We are the client | We are the server |
| `requests.get(url)` | `@app.route("/tasks")` |
| We parse responses | We build responses |

---

## Discussion Questions

1. What happens between the moment a browser hits Enter and the moment it shows a response?
2. In our Day 1 services — which part was HTTP? Which part was logic?
3. What should a server do when it receives bad data?

---

## Key Vocabulary

| Term | Meaning |
|------|---------|
| Route | A URL path mapped to a function |
| Handler | The function that runs for a route |
| Endpoint | A route + HTTP method combination |
| Payload | The data sent in a request body |
