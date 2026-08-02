# Branch Management

## What to Teach
- Keep your branch list clean — delete branches after merging
- `-d` is safe (refuses to delete unmerged branches); `-D` is forced
- Use `--merged` to find branches that can safely be deleted
- Naming conventions help teams stay organized

## Demo Steps
1. Show `git branch` with several branches
2. Merge a branch, then delete it with `-d`
3. Try to delete an unmerged branch with `-d` — show the error
4. Show `git branch --merged` to find cleanup candidates
5. Rename a branch with `-m`
6. Discuss naming conventions

## Key Points
- Deleted branches are just removed pointers — the commits still exist (recoverable via reflog)
- `git branch --merged` is your cleanup tool: merged branches are safe to delete
- Consistent naming conventions matter for team collaboration and CI/CD (e.g., auto-deploy from `release/*`)

## Common Student Questions
- **Q: Is it safe to delete a merged branch?**
  - A: Yes! The commits are already part of the target branch. The branch name is just a label.

- **Q: Can I recover a deleted branch?**
  - A: Yes, using `git reflog` to find the last commit and `git branch <name> <hash>` to recreate it.

- **Q: Who decides the naming convention?**
  - A: The team. It is usually documented in the project's contributing guide or README.

## Tips
- Regularly run `git branch --merged | grep -v main` to find stale branches
- In a DevOps context, branch names often trigger CI/CD pipelines (e.g., `release/*` triggers deploy)
- GitHub auto-suggests deleting a branch after a PR is merged
