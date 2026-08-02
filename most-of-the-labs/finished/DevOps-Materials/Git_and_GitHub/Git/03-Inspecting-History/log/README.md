# Git Log

## What to Teach
- `git log` is your window into project history
- Different formats for different needs: `--oneline` for quick scan, `--stat` for file changes, `-p` for full diffs
- `--graph --all` is essential when working with branches
- Filtering options: by author, date, message content

## Demo Steps
1. In a repo with several commits, run `git log` — show the full output
2. Show `git log --oneline` for compact view
3. Create a couple of branches with commits, then show `git log --oneline --graph --all`
4. Demo filtering: `--author`, `--since`, `--grep`
5. Show `git show HEAD` to inspect a single commit
6. Suggest setting up a `git lg` alias for the pretty log

## Key Points
- `HEAD` refers to the current commit you are on
- `HEAD~1` means "one commit before HEAD", `HEAD~2` means two back, etc.
- `--all` shows commits from ALL branches, not just the current one
- `--graph` draws the branch structure in ASCII
- `git show <hash>` displays a single commit's details and diff

## Common Student Questions
- **Q: How do I find who changed a specific line?**
  - A: Use `git blame <file>` — shows the last commit that modified each line.

- **Q: Can I search for changes to a specific file?**
  - A: Yes! `git log -- path/to/file` shows only commits that touched that file.

- **Q: What does HEAD mean?**
  - A: HEAD is a pointer to the current commit. It usually points to the tip of the current branch.

## Tips
- Encourage students to create an alias: `git config --global alias.lg "log --oneline --graph --all --decorate"`
- The graph view is especially powerful when teaching branching later
- `git log` uses a pager (less) — press `q` to exit, `/` to search
