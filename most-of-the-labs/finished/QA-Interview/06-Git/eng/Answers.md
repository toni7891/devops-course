# Git & GitHub Interview Answers

**Q1. What is Git and why is it used?**
Git is a distributed version control system that tracks changes in source code. It allows multiple developers to work on the same project simultaneously, maintains a full history of changes, and supports branching and merging for parallel development.

**Q2. What is the difference between Git and GitHub?**
Git is a local version control tool that runs on your machine. GitHub is a cloud-based hosting platform for Git repositories that adds collaboration features like pull requests, issue tracking, and access control.

**Q3. What is a Git repository?**
A repository (repo) is a directory tracked by Git. It contains all project files plus a hidden `.git` folder that stores the entire history, branches, and configuration. Repos can be local (on your machine) or remote (on GitHub, GitLab, etc.).

**Q4. What is the difference between `git init` and `git clone`?**
`git init` creates a new empty repository in the current directory. `git clone <url>` copies an existing remote repository to your local machine, including all its history and branches.

**Q5. What are the three stages (areas) in Git?**

1. **Working Directory** — where you edit files.
2. **Staging Area (Index)** — where you place changes ready to be committed (`git add`).
3. **Repository (.git)** — where committed snapshots are permanently stored (`git commit`).

**Q6. What is the difference between `git add` and `git commit`?**
`git add` moves changes from the working directory to the staging area. `git commit` takes everything in the staging area and saves it as a permanent snapshot in the repository history.

**Q7. What is the difference between `git pull` and `git fetch`?**
`git fetch` downloads new data from the remote repository but does not merge it into your working branch. `git pull` does both — it fetches and then automatically merges the remote changes into your current branch. Essentially, `git pull` = `git fetch` + `git merge`.

**Q8. What is the difference between `git merge` and `git rebase`?**
Both integrate changes from one branch into another. `git merge` creates a new merge commit that combines the two branches, preserving the full history. `git rebase` replays your commits on top of the target branch, producing a linear history. Merge is safer for shared branches; rebase is cleaner for local/feature branches.

**Q9. What is a merge conflict and how do you resolve it?**
A merge conflict occurs when Git cannot automatically combine changes because two branches modified the same lines in a file. To resolve it: open the conflicted file, look for the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), choose the correct code, remove the markers, then `git add` the file and `git commit`.

**Q10. What is a Git branch and why do we use branches?**
A branch is a lightweight pointer to a commit. Branches let developers work on features, bug fixes, or experiments in isolation without affecting the main codebase. Once the work is complete and tested, it can be merged back.

**Q11. How do you create, switch, and delete branches in Git?**

- Create: `git branch <name>` or `git checkout -b <name>` (create and switch).
- Switch: `git checkout <name>` or `git switch <name>`.
- Delete locally: `git branch -d <name>` (safe) or `git branch -D <name>` (force).
- Delete remote: `git push origin --delete <name>`.

**Q12. What is `HEAD` in Git?**
`HEAD` is a pointer to the current commit you are working on. It usually points to the latest commit on the current branch. When you switch branches, `HEAD` moves to point to the tip of the new branch.

**Q13. What is a detached HEAD state?**
Detached HEAD means `HEAD` is pointing directly to a specific commit instead of a branch. This happens when you check out a commit hash or a tag. Any new commits made in this state are not on any branch and can be lost if you switch away without creating a branch to save them.

**Q14. What is the difference between `git reset`, `git revert`, and `git checkout`?**

- `git reset` moves the branch pointer backward, potentially discarding commits (rewrites history).
- `git revert` creates a new commit that undoes a previous commit (safe for shared branches, does not rewrite history).
- `git checkout` switches branches or restores files from a specific commit without changing history.

**Q15. What are the three modes of `git reset`?**

- `--soft` — moves HEAD to the target commit; keeps changes staged and in working directory.
- `--mixed` (default) — moves HEAD; unstages changes but keeps them in the working directory.
- `--hard` — moves HEAD; discards all changes from both staging area and working directory.

**Q16. What is `git stash` and when would you use it?**
`git stash` temporarily saves uncommitted changes (both staged and unstaged) and reverts the working directory to a clean state. Use it when you need to switch branches or pull updates but aren't ready to commit your current work. Restore with `git stash pop` or `git stash apply`.

**Q17. What is a `.gitignore` file and why is it important?**
A `.gitignore` file lists patterns of files and directories that Git should not track — e.g., build artifacts, `node_modules/`, `.env` files, IDE configs. It keeps the repository clean and prevents accidental commits of sensitive or unnecessary files.

**Q18. What is the difference between a fast-forward merge and a three-way merge?**
A **fast-forward merge** happens when the target branch has no new commits since the feature branch diverged — Git simply moves the pointer forward, no merge commit needed. A **three-way merge** happens when both branches have diverged — Git creates a merge commit that combines the two lines of development.

**Q19. What is `git cherry-pick` and when is it useful?**
`git cherry-pick <commit-hash>` applies a specific commit from one branch onto another without merging the entire branch. Useful for applying a hotfix from a development branch to production, or selectively bringing in individual changes.

**Q20. What is `git bisect` and how does it help debug issues?**
`git bisect` performs a binary search through commit history to find which commit introduced a bug. You mark a known good commit and a known bad commit, then Git checks out the midpoint for you to test. It halves the search space each step, efficiently pinpointing the problematic commit in O(log n) steps.

**Q21. What is the difference between `git diff`, `git diff --staged`, and `git diff HEAD`?**

- `git diff` — shows changes in the working directory that are **not yet staged**.
- `git diff --staged` (or `--cached`) — shows changes that are **staged but not yet committed**.
- `git diff HEAD` — shows **all changes** (both staged and unstaged) compared to the last commit.

**Q22. What are Git tags? What is the difference between lightweight and annotated tags?**
Tags mark specific commits, typically used for release versions (e.g., `v1.0.0`). A **lightweight tag** is just a pointer to a commit (`git tag v1.0`). An **annotated tag** stores extra metadata — tagger name, date, and message (`git tag -a v1.0 -m "Release 1.0"`). Annotated tags are recommended for releases.

**Q23. What is a pull request (PR) and how does it fit into a team workflow?**
A pull request is a GitHub feature that lets a developer notify the team that a feature branch is ready to be merged. Team members review the code, leave comments, request changes, and approve. Once approved, the branch is merged into the main branch. PRs serve as a code review and quality gate.

**Q24. What is a fork in GitHub and how does it differ from a branch?**
A **fork** is a full copy of a repository under your own GitHub account — used for contributing to projects you don't have write access to. A **branch** is a parallel line of development within the same repository. You fork to propose changes to someone else's project; you branch to work within your own.

**Q25. What are GitHub Actions and how are they used for CI/CD?**
GitHub Actions is a built-in automation platform. You define workflows in YAML files (`.github/workflows/`) that trigger on events like push, pull request, or schedule. Common uses: run tests automatically, lint code, build and push Docker images, and deploy to production.

**Q26. What is a Git hook? Name some common hooks and their use cases.**
Git hooks are scripts that run automatically before or after Git events. They live in `.git/hooks/`. Common hooks:

- `pre-commit` — run linters or tests before allowing a commit.
- `commit-msg` — enforce commit message format.
- `pre-push` — run tests before pushing to remote.
- `post-merge` — auto-install dependencies after a merge.

**Q27. How do you squash commits and why would you do it?**
Squashing combines multiple commits into one. Use interactive rebase: `git rebase -i HEAD~n`, then mark commits as `squash` (or `s`). It keeps the history clean by collapsing noisy work-in-progress commits into a single meaningful commit before merging.

**Q28. What is `git reflog` and how can it help recover lost commits?**
`git reflog` records every movement of `HEAD` — branch switches, resets, rebases, commits. Even after a hard reset or dropped rebase, the commit still exists in the reflog for ~90 days. You can recover it with `git checkout <hash>` or `git reset --hard <hash>`.

**Q29. What is the difference between `git rm` and simply deleting a file?**
Deleting a file with `rm` removes it from the working directory but Git still tracks it — you'd need to `git add` the deletion. `git rm <file>` removes the file and stages the deletion in one step, so the next commit records the removal.

**Q30. What is a Git submodule and when would you use one?**
A Git submodule is a repository embedded inside another repository. It pins a specific commit of the external repo. Use submodules when your project depends on another Git project (e.g., a shared library) and you want to track a specific version of it independently.
