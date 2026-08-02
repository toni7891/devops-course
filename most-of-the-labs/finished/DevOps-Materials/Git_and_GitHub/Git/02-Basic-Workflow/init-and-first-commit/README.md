# Init and First Commit

## What to Teach
- `git init` creates a new Git repository in the current directory
- The `.git` folder IS the repository — it contains all history, config, and metadata
- The basic lifecycle: **create/modify file → stage (add) → commit**
- A commit is a snapshot of all staged changes at a point in time

## Demo Steps
1. Create a new empty directory and `cd` into it
2. Run `git init` — point out the `.git` folder that appears
3. Briefly show what is inside `.git` (don't go deep — just show it exists)
4. Create a `README.md` file
5. Run `git status` — show the file is "untracked" (red)
6. Run `git add README.md` — then `git status` again (green, staged)
7. Run `git commit -m "add README"` — then `git log` to see the commit
8. **Destructive demo** (optional): delete `.git` and show that Git no longer recognizes the directory

## Key Points
- `git init` only needs to be run **once** per project
- The `.git` folder should never be manually edited
- If you delete `.git`, all history is lost — the files remain but Git history is gone
- You can run `git init` inside an existing project (it won't overwrite files)

## Common Student Questions
- **Q: Can I init inside an existing project with files?**
  - A: Yes! `git init` just creates the `.git` folder. Your existing files become "untracked" and you can start adding them.

- **Q: Should I ever commit the `.git` folder?**
  - A: No. The `.git` folder is the repository itself — it should never be nested inside another repo.

- **Q: What is the difference between `git init` and `git clone`?**
  - A: `git init` creates a new empty repo locally. `git clone` copies an existing remote repo (with all its history).

## Tips
- Use this demo to establish the "create → add → commit" rhythm — students will repeat this hundreds of times
- Emphasize that `git init` is purely local — no GitHub account needed
