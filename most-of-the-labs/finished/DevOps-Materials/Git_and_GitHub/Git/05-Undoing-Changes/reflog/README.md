# Git Reflog

## What to Teach
- Reflog (reference log) records every movement of HEAD in your local repository
- It is your **safety net** — even after `reset --hard`, you can recover
- Reflog is **local only** — it is not pushed or shared
- Entries expire: reachable commits after 90 days, unreachable after 30 days

## Demo Steps
1. Show `git reflog` — walk through the output format
2. Create a "disaster" scenario: make commits, then `git reset --hard HEAD~2`
3. Show `git log` — commits appear gone
4. Show `git reflog` — the commits are still referenced
5. Recover with `git reset --hard <reflog-hash>`
6. Show alternative: `git branch recovered <hash>` to create a new branch

## Key Points
- Reflog records: commits, checkouts, resets, merges, rebases — any HEAD movement
- `HEAD@{0}` is the current position, `HEAD@{1}` is the previous, etc.
- Reflog is the answer to "I lost my commits" (as long as they were committed at some point)
- It does NOT help with uncommitted changes — if you never committed, there is nothing to recover

## Common Student Questions
- **Q: Does reflog work for things I never committed?**
  - A: No. Reflog only tracks committed snapshots. Uncommitted work that is lost with `reset --hard` is truly gone.

- **Q: Is reflog shared with the team?**
  - A: No. Reflog is strictly local. Each developer has their own reflog.

- **Q: How long do reflog entries last?**
  - A: 90 days for reachable commits, 30 days for unreachable. After that, Git's garbage collector may clean them.

## Tips
- Present reflog as the "undo for undo" — it removes fear from experimenting with Git
- This is a great time to say: "In Git, it is very hard to truly lose committed work"
- Pair this with the reset demo: reset hard → panic → reflog → recover → relief
