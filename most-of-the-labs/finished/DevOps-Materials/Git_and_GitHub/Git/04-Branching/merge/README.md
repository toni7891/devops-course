# Merge

## What to Teach
- Merge combines the work from one branch into another
- Two types of merge:
  - **Fast-forward**: main has no new commits → just moves the pointer (no merge commit)
  - **Three-way merge**: both branches have new commits → creates a merge commit with two parents
- Always switch to the **target** branch first (the one you want to merge INTO)

## Demo Steps
1. Create a feature branch, make a commit, switch to main, merge → show **fast-forward**
2. Create another feature branch, make commits on BOTH branches → merge shows **three-way merge**
3. Use `git log --oneline --graph` after each merge to visualize
4. Emphasize: "I am ON main, I merge feature INTO main"

## Key Points
- `git merge <branch>` merges the specified branch INTO the current branch
- Fast-forward = linear history (clean but loses branch context)
- Three-way merge = preserves branch history (you can see when work was branched and merged)
- The merge commit has two parent commits
- You can force a merge commit even on fast-forward with `--no-ff`

## Common Student Questions
- **Q: What is a merge commit?**
  - A: A special commit with two parents that records the point where two branches were combined.

- **Q: Which branch should I be on when merging?**
  - A: The branch you want to merge INTO. Typically you switch to `main` and then merge your feature branch.

- **Q: Does merge delete the feature branch?**
  - A: No. After merging, the branch still exists. You can delete it manually with `git branch -d`.

## Tips
- Draw the commit graph on a whiteboard to show fast-forward vs three-way merge
- Always use `git log --graph` after merging to reinforce the visual model
- Mention `--no-ff` flag: forces a merge commit even when fast-forward is possible (useful for preserving feature branch history)
