# What is Git?

## What to Teach
- **Version Control** is a system that records changes to files over time so you can recall specific versions later
- **Why it matters for DevOps**: collaboration, traceability, rollback, automation (CI/CD depends on it)
- **Centralized vs Distributed**: Git is distributed — every developer has the full history locally
- **Why Git won**: speed, powerful branching model, open source, used by virtually every tech company
- Analogy: "Save points in a video game" — you can always go back to a previous state

## Demo Steps
1. Show `git --version` to verify installation
2. Create a small project from scratch
3. Make two commits and show how `git log` records the history
4. Use `git diff` to show the difference between two points in time
5. Emphasize: without Git, you would need to manually copy folders (project_v1, project_v2, project_final_FINAL...)

## Key Points
- Git tracks **snapshots** of your project, not diffs
- Every operation is local and fast (no network needed for most commands)
- Git is the foundation of modern software development workflows
- GitHub, GitLab, Bitbucket are **hosting platforms** for Git repositories — they are NOT Git itself

## Common Student Questions
- **Q: How is Git different from Google Drive or Dropbox?**
  - A: Those sync files but don't track meaningful versions with messages. Git records *what* changed, *who* changed it, *when*, and *why* (via commit messages). You can branch, merge, and roll back precisely.

- **Q: Do I always need GitHub to use Git?**
  - A: No. Git works entirely locally. GitHub is a remote hosting service — it adds collaboration features (PRs, Issues) on top of Git.

- **Q: Is Git only for code?**
  - A: Git works best with text files (code, config, docs). It can track binary files but cannot show meaningful diffs for them.

## Tips
- Start the module by asking students: "Has anyone ever lost work because they overwrote a file?" — this motivates the need for version control
- Keep the first demo simple — don't introduce branching yet
- If students ask about GUI tools, acknowledge them but emphasize CLI fluency first (essential for DevOps)
