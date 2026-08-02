# .gitignore

## What to Teach
- `.gitignore` tells Git which files and directories to exclude from tracking
- Critical for security: **never commit secrets** (.env, API keys, credentials)
- Critical for cleanliness: don't commit dependencies (node_modules), build artifacts, OS files
- Pattern syntax: glob patterns, directory trailing slash, negation with `!`
- `.gitignore` only prevents **untracked** files from being added — already tracked files are NOT affected

## Demo Steps
1. Create a `.gitignore` with common DevOps patterns
2. Create files that match the patterns (node_modules/, .env)
3. Run `git status` — show they don't appear
4. **The "already tracked" problem**: track a file first, then add it to gitignore — show it still appears
5. Fix with `git rm --cached <file>` — explain it removes from Git but keeps the file on disk
6. Show pattern syntax with examples

## Key Points
- `.gitignore` should be one of the first files in any project
- It should be committed to the repository (so the team shares the same ignore rules)
- `git rm --cached <file>` removes a file from tracking without deleting it
- Each line in `.gitignore` is a glob pattern
- Lines starting with `#` are comments
- Lines starting with `!` negate a previous pattern

## Common Student Questions
- **Q: I already committed .env with secrets. Now what?**
  - A: Add `.env` to `.gitignore`, run `git rm --cached .env`, commit. But the secret is still in the Git history! You should rotate the secret and consider using `git filter-branch` or BFG Repo Cleaner to purge it from history.

- **Q: Can I have a global gitignore?**
  - A: Yes! `git config --global core.excludesfile ~/.gitignore_global` — useful for OS files (.DS_Store, Thumbs.db) and editor files.

- **Q: Where can I find gitignore templates?**
  - A: github.com/github/gitignore has templates for every language and framework. Also: gitignore.io

## Tips
- Stress the security angle: leaked `.env` files and API keys are one of the most common security incidents
- Show the GitHub gitignore template collection
- Mention that `.gitignore` patterns are relative to the location of the `.gitignore` file
