# Git Diff

## What to Teach
- `git diff` compares different states of files in Git
- Three key comparisons:
  - `git diff` → working directory vs staging area (unstaged changes)
  - `git diff --staged` → staging area vs last commit (what will be committed)
  - `git diff HEAD` → working directory vs last commit (all changes)
- Can also compare branches and specific commits

## Demo Steps
1. Create a file and commit it
2. Modify the file — run `git diff` (shows unstaged changes)
3. Stage it — run `git diff` (empty!) then `git diff --staged` (shows staged changes)
4. Modify the file again — now show all three: `git diff`, `git diff --staged`, `git diff HEAD`
5. Explain the diff output format: `---`, `+++`, `@@` hunk headers, `-` removed, `+` added
6. Show `git diff main..branch` for branch comparison

## Key Points
- `git diff` with no arguments shows ONLY unstaged changes
- `git diff --staged` shows ONLY staged changes (ready to commit)
- The `@@` line shows which lines are affected (old line numbers, new line numbers)
- `..` compares tips of two branches; `...` compares since the branches diverged

## Common Student Questions
- **Q: Why does `git diff` show nothing after I staged my changes?**
  - A: Because `git diff` compares working directory to staging area. After staging, they are the same. Use `git diff --staged` to see what is staged.

- **Q: What does the `@@` line mean?**
  - A: `@@ -1,3 +1,4 @@` means: in the old file, starting at line 1 showing 3 lines; in the new file, starting at line 1 showing 4 lines.

## Tips
- Encourage using VS Code's built-in diff viewer during class for better visual clarity
- Reinforce the three-area model: `diff` relates to the same working directory → staging → repo concept
