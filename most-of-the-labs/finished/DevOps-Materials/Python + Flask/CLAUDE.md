# Python + Flask Course — Instructor Workspace

## Context

This is a 5-day intensive Python + Flask course for developers.
Each day is a numbered folder under `Day-X-<topic>/`.
Topics progress from API fundamentals → Flask → advanced patterns.

## Content Rules

- All text (README, comments, docstrings, variable names) must be in **English**
- Folders are numbered: `1-What-Is-API/`, `2-HTTP-Protocol/`, etc.
- Every topic folder must have a `README.md` with: time block, objectives, topics, and exercises
- Python code must be complete and runnable — no pseudo-code
- No Hebrew in any file

## Folder Conventions

```
Day-X-<topic>/
  README.md                  ← day overview with schedule table
  1-<topic>/
    README.md                ← instructor guide for this block
    <exercise>.py            ← runnable code
  ...
  6-<final-exercise>/
    core/
    main.py
    README.md
  7-Evening-Assignment/
    services/
    core/
    main.py
    README.md
```

## Code Conventions

- All API calls go through `make_request()` — never call `requests` directly in service layers
- Every function returns `{"success": bool, "data": ...}` or `{"success": False, "error": "..."}`
- Decorators: always `@log_execution` above `@handle_errors`
- Caching: in-memory dict, keyed by resource name
- Retry: `MAX_RETRIES = 2`, sleep 1s between attempts

## Custom Commands

- `/new-day` — scaffold a new day folder from a lesson plan
- `/new-topic` — scaffold a single numbered topic folder
- `/review-day` — review a day's content for quality and consistency

## Agents

- `content-reviewer` — reviews exercise quality, checks English-only, validates runnable code
