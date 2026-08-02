#!/bin/bash
# Topic: Git Diff
# Description: Comparing changes between states

# --- Setup ---
echo "line 1" > example.txt
git add example.txt && git commit -m "add example"

echo "line 2" >> example.txt

# --- Diff: Working Directory vs Staging Area (unstaged changes) ---
git diff

# --- Stage the Change ---
git add example.txt

# --- Diff: Staging Area vs Last Commit (staged changes) ---
git diff --staged
# (same as: git diff --cached)

# --- Diff: Working Directory vs Last Commit ---
git diff HEAD

# --- After More Changes ---
echo "line 3" >> example.txt

# Now there are both staged and unstaged changes
git diff          # shows only unstaged (line 3)
git diff --staged # shows only staged (line 2)
git diff HEAD     # shows both

# --- Compare Branches ---
git diff main..feature-branch
git diff main...feature-branch  # changes since branches diverged

# --- Compare Specific Commits ---
git diff abc1234..def5678

# --- Diff for a Specific File ---
git diff -- path/to/file.txt

# --- Show Only File Names ---
git diff --name-only
git diff --name-status  # also shows A(dded), M(odified), D(eleted)

# --- Word-level Diff ---
git diff --word-diff
