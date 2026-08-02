# Git Revert

## What to Teach
- `git revert` creates a **new commit** that undoes the changes from a previous commit
- Unlike `reset`, it does NOT rewrite history — safe for shared branches
- The original commit remains in the history (for traceability)

## Demo Steps
1. Create 3 commits including one "buggy" commit
2. `git revert HEAD` — show the new revert commit in the log
3. Show that the original commit is still in history
4. Demo `--no-commit` for more control
5. Compare with reset: "reset removes history, revert adds to history"

## Key Points
- Revert is the **safe** way to undo changes on shared/pushed branches
- It creates a new commit — history is preserved and everyone can see what was undone
- You can revert any commit, not just the latest one
- Reverting a merge commit requires `-m` to specify which parent to keep

## Common Student Questions
- **Q: When should I use revert vs reset?**
  - A: **Revert** for commits that have been pushed/shared (preserves history). **Reset** for local-only commits (rewrites history).

- **Q: Can I revert a revert?**
  - A: Yes! Just revert the revert commit. This effectively re-applies the original changes.

- **Q: What if reverting causes a conflict?**
  - A: Resolve it just like a merge conflict, then `git add` and `git commit`.

## Tips
- Stress the "shared branch" rule: if others have pulled the commit, use revert, not reset
- Show `git log` after revert to prove the original commit still exists
