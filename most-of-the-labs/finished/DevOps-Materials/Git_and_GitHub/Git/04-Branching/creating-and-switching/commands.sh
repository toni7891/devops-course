#!/bin/bash
# Topic: Creating and Switching Branches
# Description: Working with Git branches

# --- List Branches ---
git branch         # local branches
git branch -a      # all branches (including remote)
git branch -v      # branches with last commit info

# --- Create a New Branch ---
git branch feature-login

# --- Switch to a Branch ---
git switch feature-login
# or (older command, still works):
git checkout feature-login

# --- Create and Switch in One Command ---
git switch -c feature-signup
# or:
git checkout -b feature-payment

# --- See Which Branch You Are On ---
git branch  # asterisk (*) marks current branch
git status  # shows "On branch ..."

# --- Demo: Branches Are Isolated ---
# On feature-login branch
echo "login page" > login.html
git add login.html && git commit -m "add login page"

# Switch back to main
git switch main
ls  # login.html does not exist here!

# Switch back to feature-login
git switch feature-login
ls  # login.html is here

# --- Visualize ---
git log --oneline --graph --all
