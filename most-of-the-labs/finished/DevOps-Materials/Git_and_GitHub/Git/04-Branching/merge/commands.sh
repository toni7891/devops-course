#!/bin/bash
# Topic: Merge
# Description: Combining branches with git merge

# --- Setup: Create a Feature Branch ---
git switch -c feature-navbar
echo "<nav>Home | About</nav>" > navbar.html
git add navbar.html && git commit -m "add navbar"

# --- Fast-Forward Merge ---
# If main has no new commits since the branch was created
git switch main
git merge feature-navbar
# Result: main simply moves forward to the same commit
git log --oneline --graph --all

# --- Three-Way Merge ---
# Setup: both branches have new commits
git switch -c feature-footer
echo "<footer>Copyright 2024</footer>" > footer.html
git add footer.html && git commit -m "add footer"

git switch main
echo "Welcome to our site" > index.html
git add index.html && git commit -m "add homepage"

# Now main and feature-footer have diverged
git log --oneline --graph --all

# Merge creates a new "merge commit"
git merge feature-footer
# Result: a merge commit with two parents
git log --oneline --graph --all

# --- Verify Merge ---
ls  # both navbar.html, footer.html, and index.html exist

# --- Merge with a Custom Message ---
git merge feature-branch -m "merge feature-branch into main"
