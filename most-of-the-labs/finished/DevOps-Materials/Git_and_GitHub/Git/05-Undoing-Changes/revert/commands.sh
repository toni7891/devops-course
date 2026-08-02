#!/bin/bash
# Topic: Git Revert
# Description: Safely undoing changes by creating a new commit

# --- Setup ---
echo "feature A" > feature.txt && git add . && git commit -m "add feature A"
echo "feature B" >> feature.txt && git add . && git commit -m "add feature B"
echo "buggy code" >> feature.txt && git add . && git commit -m "add buggy code"
git log --oneline

# --- Revert the Last Commit ---
git revert HEAD
# Opens editor for the revert commit message (default: "Revert 'add buggy code'")
git log --oneline  # new revert commit appears

# --- Revert a Specific Commit (not the latest) ---
git log --oneline  # find the hash
git revert abc1234  # reverts that specific commit

# --- Revert Without Auto-Committing ---
git revert --no-commit HEAD
git status  # changes are staged but not committed
# You can modify further, then commit manually
git commit -m "revert buggy code and fix related issue"

# --- Revert a Merge Commit ---
# git revert -m 1 <merge-commit-hash>
# -m 1 means: keep the first parent (usually main)
