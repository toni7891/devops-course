#!/bin/bash
# Topic: Git Reset
# Description: Undoing commits by moving the branch pointer

# --- Setup ---
echo "v1" > app.txt && git add app.txt && git commit -m "version 1"
echo "v2" > app.txt && git add app.txt && git commit -m "version 2"
echo "v3" > app.txt && git add app.txt && git commit -m "version 3"
git log --oneline  # shows 3 commits

# --- Soft Reset: undo commit, keep changes staged ---
git reset --soft HEAD~1
git status  # "version 3" change is staged (green)
git log --oneline  # "version 3" commit is gone

# Re-commit to restore for next demo
git commit -m "version 3"

# --- Mixed Reset (default): undo commit, keep changes unstaged ---
git reset HEAD~1
# same as: git reset --mixed HEAD~1
git status  # "version 3" change is in working directory (red)
git log --oneline  # "version 3" commit is gone

# Re-add and commit
git add app.txt && git commit -m "version 3"

# --- Hard Reset: undo commit, DISCARD all changes ---
git reset --hard HEAD~1
git status  # clean — "version 3" changes are GONE
git log --oneline  # "version 3" commit is gone
cat app.txt  # shows "v2"

# --- Unstage a File (without undoing commit) ---
echo "new change" >> app.txt
git add app.txt
git status  # staged
git reset HEAD app.txt  # unstage
git status  # unstaged (change still exists in working directory)

# --- Reset to a Specific Commit ---
git reset --hard abc1234  # go back to any commit by hash
