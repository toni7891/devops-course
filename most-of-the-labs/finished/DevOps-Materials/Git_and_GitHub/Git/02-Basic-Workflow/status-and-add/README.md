# Status and Add

## What to Teach
- **The Three Areas** — this is the most important mental model in Git:
  1. **Working Directory**: your actual files on disk
  2. **Staging Area (Index)**: a preparation area for the next commit
  3. **Repository (.git)**: the committed history
- File states: **untracked** → **staged** → **committed** → **modified** → **staged** → ...
- `git status` shows which files are in which state
- `git add` moves changes from working directory to staging area

## Demo Steps
1. Create a repo with 3 files — show `git status` (all untracked)
2. Add one file — show status (one green, two red)
3. Add the rest and commit
4. Modify a file — show status (modified, red)
5. Stage it — show status (green)
6. Demo `git add .` to stage everything
7. Demo `git restore --staged` to unstage
8. **Draw the three areas on a whiteboard** — this visual is essential

## Key Points
- `git add` does NOT mean "add a new file" — it means "add these changes to the staging area"
- `git add .` adds everything in the current directory and below
- `git add -A` adds everything in the entire repo (regardless of current directory)
- The staging area lets you craft commits precisely — you don't have to commit everything at once
- `git restore --staged <file>` unstages without losing the changes

## Common Student Questions
- **Q: Why do we need a staging area? Why not just commit directly?**
  - A: The staging area lets you choose exactly what goes into each commit. You might have changed 5 files but only want to commit 3 of them as one logical change.

- **Q: What is the difference between `git add .` and `git add -A`?**
  - A: `git add .` stages changes from the current directory down. `git add -A` stages all changes in the entire repository. In most cases they do the same thing if you are at the repo root.

- **Q: I modified a file but `git status` doesn't show it?**
  - A: The file might not be tracked by Git yet, or you might be in a different directory. Always check with `git status`.

## Tips
- Draw the three-area diagram on the whiteboard — refer back to it throughout the entire Git module
- Color coding: red = not staged, green = staged (same as terminal output)
- Have students practice the cycle: modify → status → add → status → commit
