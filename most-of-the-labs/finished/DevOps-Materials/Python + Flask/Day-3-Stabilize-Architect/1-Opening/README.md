# Topic 1 — Day Opening & Goal Setting

**Time:** 09:30–10:00 (30 min)

---

## Instructor Script

Open with this framing:

> "Yesterday you built an API. Today you are going to make it production-worthy.
> A real developer doesn't just make code work — they make it handle everything that can go wrong."

---

## What Students Must Deliver by End of Day

| Deliverable | Part | What It Is |
|-------------|------|------------|
| Stable CRUD API | Part 1 | Working endpoints + edge case handling |
| Postman Collection | Part 1 | Demonstrates all CRUD flows |
| `error_handling_notes.md` | Part 2 | Research doc on Flask global handlers |
| Refactored app structure | Part 3 | Clean `routes/services/models/` split |

---

## How They Will Be Evaluated

1. **Does the API handle bad input gracefully?** — No 500 errors from user mistakes
2. **Are error responses consistent?** — Always `{"success": false, "error": {"message": "...", "code": "..."}}`
3. **Is the code separated by responsibility?** — No logic in routes, no HTTP in services
4. **Can the storage layer be swapped for a DB without touching routes?** — That is the test

---

## The Three-Part Frame

Draw this on the board:

```
Part 1: FIX     → Your API should not crash on bad input
Part 2: LEARN   → Understand how Flask handles errors globally
Part 3: BUILD   → Restructure for the database that is coming tomorrow
```

---

## Opening Question

Ask the class before starting Part 1:

> "What happens when someone calls DELETE /tasks/999 on your Day 2 code?"

Let them answer. Then:

> "If it crashes with a 500, that is a bug. If it returns a clear 404, that is a feature.
> Today we make that distinction everywhere."
