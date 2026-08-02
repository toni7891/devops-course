# Creating and Switching Branches

## What to Teach
- A branch is a lightweight **pointer** to a commit — creating a branch is instant
- Branches allow parallel development without affecting the main codebase
- `git switch` is the modern way to change branches (Git 2.23+); `git checkout` still works
- `git switch -c` creates a new branch and switches to it in one step

## Demo Steps
1. Show `git branch` — only `main` exists
2. Create `feature-login` branch: `git branch feature-login`
3. Switch to it: `git switch feature-login`
4. Make a commit on the feature branch (add a file)
5. Switch back to `main` — show that the new file **does not exist** on main
6. Switch back to feature — file is back
7. Show `git log --oneline --graph --all` to visualize both branches

## Key Points
- Branches are just pointers to commits — they are cheap and fast to create
- `HEAD` points to the current branch, which points to a commit
- Creating a branch does NOT switch to it (unless you use `-c` / `-b`)
- Always know which branch you are on before making commits

## Common Student Questions
- **Q: What happens to my uncommitted changes when I switch branches?**
  - A: Git will try to carry them over. If there is a conflict, Git will prevent the switch. Options: commit first, stash, or discard changes.

- **Q: What is the difference between `switch` and `checkout`?**
  - A: `switch` is focused on branch switching only. `checkout` does multiple things (switch branches, restore files, etc.). `switch` was introduced to reduce confusion.

- **Q: Can I have unlimited branches?**
  - A: Yes. Branches are nearly free in Git. Use them liberally.

## Tips
- Use `switch` consistently in demos to teach modern Git
- Emphasize the isolation — this is what makes branches powerful
- Branch naming conventions: `feature/`, `bugfix/`, `hotfix/`, `release/`
