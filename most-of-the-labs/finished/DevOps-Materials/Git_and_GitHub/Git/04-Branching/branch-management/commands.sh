#!/bin/bash
# Topic: Branch Management
# Description: Organizing and maintaining branches

# --- List Branches ---
git branch          # local branches
git branch -a       # all branches (local + remote)
git branch -v       # with last commit info
git branch -vv      # with tracking info

# --- Delete a Merged Branch ---
git branch -d feature-done
# Safe delete: only works if the branch has been merged

# --- Force Delete an Unmerged Branch ---
git branch -D feature-abandoned
# WARNING: this deletes unmerged work

# --- Rename a Branch ---
git branch -m old-name new-name
# Rename current branch:
git branch -m new-name

# --- Find Merged/Unmerged Branches ---
git branch --merged         # branches already merged into current
git branch --no-merged      # branches NOT yet merged

# --- Branch Naming Conventions ---
# feature/user-authentication
# bugfix/login-redirect
# hotfix/security-patch
# release/v1.2.0
# chore/update-dependencies
