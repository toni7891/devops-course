# Commit

## What to Teach
- A commit is a **snapshot** of the staging area at a point in time
- Each commit has: a unique **SHA hash**, **author**, **timestamp**, **message**, and a pointer to the **parent commit**
- Commit messages should be meaningful — they are documentation for your team and future self
- Convention: use imperative mood ("add feature" not "added feature")

## Demo Steps
1. Make a change, stage it, commit with `-m`
2. Show `git log` to see the commit
3. Show `git log --oneline` for compact view
4. Demo `git commit` without `-m` — editor opens for multi-line message
5. Demo `git commit -am` shortcut — explain the caveat (tracked files only)
6. Show examples of bad vs good commit messages
7. Show `git show HEAD` to see what a commit contains

## Key Points
- Every commit creates an immutable snapshot (you can always go back)
- The commit hash (SHA) uniquely identifies each commit
- `HEAD` is a pointer to the current commit (the latest on your branch)
- `-am` is a shortcut but **does not add untracked files** — common source of confusion
- Small, focused commits are better than large, mixed ones

## Common Student Questions
- **Q: Can I undo a commit?**
  - A: Yes — `git revert` (safe, creates a new commit) or `git reset` (rewrites history). Covered later in the module.

- **Q: What is a good commit size?**
  - A: One logical change. If you can't describe it in one sentence, it might be too big.

- **Q: What does the hash mean?**
  - A: It's a SHA-1 checksum of the commit content. It guarantees integrity — if anything changes, the hash changes.

## Tips
- Show a real open-source project's commit history (e.g., on GitHub) to demonstrate good practices
- Enforce commit message discipline from day one — it pays off during code review and debugging
- Mention conventional commits format if time permits (feat:, fix:, docs:, etc.)
