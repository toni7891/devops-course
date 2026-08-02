# Git Reset

## What to Teach
- `git reset` moves the branch pointer backward, effectively "undoing" commits
- Three modes control what happens to the changes:
  - `--soft`: changes stay **staged** (ready to re-commit)
  - `--mixed` (default): changes stay in **working directory** (unstaged)
  - `--hard`: changes are **discarded** entirely
- Think of it as: which of the three areas do you want to reset?

## Demo Steps
1. Create 3 commits (v1, v2, v3)
2. `git reset --soft HEAD~1` → show changes are still staged
3. Re-commit, then `git reset HEAD~1` (mixed) → show changes are unstaged
4. Re-commit, then `git reset --hard HEAD~1` → show changes are gone
5. **Draw the three areas diagram**: show where changes end up with each mode
6. Show `git reset HEAD <file>` for unstaging

## Key Points
- `--soft` = undo commit only (staging area and working directory unchanged)
- `--mixed` = undo commit + unstage (working directory unchanged)
- `--hard` = undo everything (DESTRUCTIVE — changes are lost)
- `HEAD~1` means "one commit back", `HEAD~2` means two back
- Reset rewrites history — **never use on shared/pushed commits**

## Common Student Questions
- **Q: I did `reset --hard` by accident. Can I recover?**
  - A: Yes! `git reflog` shows all previous HEAD positions. Use `git reset --hard <reflog-hash>` to recover.

- **Q: What is the difference between reset and revert?**
  - A: Reset rewrites history (removes commits). Revert creates a NEW commit that undoes changes. Use revert on shared branches, reset on local-only work.

- **Q: When should I use each mode?**
  - A: `--soft`: want to re-commit with a different message or combine commits. `--mixed`: want to re-stage selectively. `--hard`: want to completely discard.

## Tips
- Always emphasize: `--hard` is destructive — use with caution
- Draw the three-area diagram and show arrows for each reset mode
- Mention reflog as the safety net (covered in detail in the reflog section)
