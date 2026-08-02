# Contributing Guide — Fork & Clone Workflow for Large Teams

> Best practices for teams with 20+ contributors working on a shared GitHub repository.

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Forking the Repository](#forking-the-repository)
- [Cloning Your Fork](#cloning-your-fork)
- [Keeping Your Fork in Sync](#keeping-your-fork-in-sync)
- [Branch Strategy](#branch-strategy)
- [Pull Request Workflow](#pull-request-workflow)
- [Code Review Standards](#code-review-standards)
- [Commit Message Convention](#commit-message-convention)
- [CI/CD & Protected Branches](#cicd--protected-branches)
- [Common Mistakes to Avoid](#common-mistakes-to-avoid)

---

## Overview

With 20+ contributors, an unstructured workflow quickly leads to merge conflicts, broken builds, and lost work. This guide enforces a **Fork → Branch → PR → Review → Merge** cycle that keeps the main repository clean and all contributors in sync.

**Golden rules:**

1. Never push directly to `main` or `develop`.
2. Always work off a fresh, synced branch.
3. One feature/fix = one pull request.
4. PRs require at least **2 approvals** before merging.

---

## Repository Structure

```
upstream (org/repo)          ← shared, protected
    └── main                 ← production-ready
    └── develop              ← integration branch (default PR target)

origin (your-username/repo)  ← your personal fork
    └── develop              ← mirrors upstream/develop
    └── feature/your-feature ← your working branch
```

---

## Forking the Repository

**Do this once.**

1. Navigate to the upstream repository on GitHub.
2. Click **Fork** → **Create fork** (keep "Copy the `main` branch only" unchecked to get all branches).
3. Your fork is now at `https://github.com/YOUR_USERNAME/REPO_NAME`.

> **Do not fork another contributor's fork.** Always fork from the canonical upstream repository.

---

## Cloning Your Fork

```bash
# 1. Clone YOUR fork (not the upstream repo)
git clone git@github.com:YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME

# 2. Add the upstream remote so you can pull future changes
git remote add upstream git@github.com:ORG_NAME/REPO_NAME.git

# 3. Verify remotes
git remote -v
# origin    git@github.com:YOUR_USERNAME/REPO_NAME.git (fetch)
# origin    git@github.com:YOUR_USERNAME/REPO_NAME.git (push)
# upstream  git@github.com:ORG_NAME/REPO_NAME.git (fetch)
# upstream  git@github.com:ORG_NAME/REPO_NAME.git (push)
```

> **SSH vs HTTPS:** Prefer SSH for cloning. It avoids repeated password prompts and works seamlessly with GitHub's 2FA requirements.

---

## Keeping Your Fork in Sync

Do this **before starting any new branch** and **before opening a PR**.

```bash
# Fetch all changes from upstream
git fetch upstream

# Switch to your develop branch
git checkout my-develop-branch

# Merge upstream changes in (fast-forward preferred)
git merge upstream/my-develop-branch --ff-only

# Push the updated develop to your fork
git push origin my-develop-branch
```

> **Tip:** If `--ff-only` fails, your local branch has diverged. Use `git rebase upstream/develop` instead, then force-push with `git push origin develop --force-with-lease`.

---

## Branch Strategy

| Branch | Purpose | Who pushes? |
|---|---|---|
| `main` | Stable releases | Maintainers only (via PR) |
| `develop` | Integration / staging | Maintainers only (via PR) |
| `feature/issue-123-short-desc` | New features | Contributors (on their fork) |
| `fix/issue-456-short-desc` | Bug fixes | Contributors (on their fork) |
| `chore/update-deps` | Non-functional changes | Contributors (on their fork) |
| `hotfix/critical-bug` | Urgent prod fixes | Maintainers only |

### Creating a working branch

```bash
# Always branch off of the latest upstream/develop
git fetch upstream
git checkout -b feature/issue-42-user-auth upstream/develop
```

---

## Pull Request Workflow

1. **Sync your fork** (see above).
2. **Create a branch** from `upstream/develop`.
3. **Make small, focused commits** (see commit convention below).
4. **Push your branch** to your fork:
   ```bash
   git push origin feature/issue-42-user-auth
   ```
5. **Open a PR** from your fork's branch → `upstream/develop`.
6. **Fill out the PR template** — link the issue, describe changes, add screenshots if relevant.
7. **Request reviewers** — tag at least 2 team members.
8. **Address review comments** with new commits (do not force-push during active review).
9. **Squash and merge** once approved (maintainer responsibility).

> **Draft PRs:** Open a draft PR early if you want early feedback or want to signal work-in-progress to teammates.

---

## Code Review Standards

- Reviewers should respond within **1 business day**.
- Focus comments on the code, not the author.
- Use GitHub's **"Request changes"** for blockers; **"Comment"** for suggestions.
- Approve only when you would be comfortable shipping the code yourself.
- Maintainers resolve merge conflicts — not reviewers.

---

## Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(optional scope): <short description>

[optional body]

[optional footer: closes #issue]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**

```
feat(auth): add OAuth2 login support

Implements GitHub OAuth flow. Closes #42.
```

```
fix(api): handle null response from user endpoint
```

> Keep the subject line under 72 characters. Use the body to explain *why*, not *what*.

---

## CI/CD & Protected Branches

The following branch protections are enforced on `main` and `develop`:

- ✅ Require PR before merging
- ✅ Require at least 2 approving reviews
- ✅ Require status checks to pass (lint, tests, build)
- ✅ Require branches to be up to date before merging
- ✅ Restrict who can push (maintainers only)
- ✅ Dismiss stale reviews on new commits

Do not ask maintainers to bypass these rules — they exist for everyone's protection.

---

## Common Mistakes to Avoid

| Mistake | Correct approach |
|---|---|
| Cloning upstream directly and pushing | Fork first, then clone your fork |
| Working on `develop` or `main` directly | Always create a feature branch |
| Opening a PR without syncing first | Fetch + merge/rebase upstream before PR |
| Committing directly to a PR during review | Add new commits; don't amend + force-push |
| One giant PR with many unrelated changes | One PR per issue/feature |
| Leaving forks stale for weeks | Sync with upstream at least weekly |
| Merging your own PR | At least one other person must approve |

---

## Questions?

Open a [Discussion](../../discussions) or ping the `#dev-workflow` channel in Slack.
