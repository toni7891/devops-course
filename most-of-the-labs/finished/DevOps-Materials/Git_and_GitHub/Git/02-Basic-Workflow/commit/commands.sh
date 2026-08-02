#!/bin/bash
# Topic: Commit
# Description: Creating commits and writing good commit messages

# --- Basic Commit ---
git commit -m "add user authentication feature"

# --- Commit with Editor (opens VS Code or default editor) ---
git commit
# This opens the editor for a multi-line message:
# Line 1: Short summary (50 chars max)
# Line 2: blank
# Line 3+: Detailed description

# --- Shortcut: Stage and Commit Tracked Files ---
git commit -am "fix login validation bug"
# WARNING: -am only stages TRACKED files (won't add new untracked files)

# --- View Commit History ---
git log
git log --oneline

# --- Anatomy of a Commit ---
git log -1  # Shows: hash, author, date, message
git show HEAD  # Shows the commit details + diff

# --- Good vs Bad Commit Messages ---
# BAD:
# git commit -m "fix"
# git commit -m "update"
# git commit -m "asdfgh"
# git commit -m "WIP"

# GOOD:
# git commit -m "fix password validation for special characters"
# git commit -m "add email notification on order completion"
# git commit -m "remove deprecated API endpoint /v1/users"
