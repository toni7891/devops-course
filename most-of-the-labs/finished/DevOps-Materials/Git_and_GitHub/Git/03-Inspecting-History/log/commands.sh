#!/bin/bash
# Topic: Git Log
# Description: Viewing and navigating commit history

# --- Basic Log ---
git log

# --- Compact View ---
git log --oneline

# --- Graphical View (essential for branches) ---
git log --oneline --graph --all

# --- Decorated (show branch/tag names) ---
git log --oneline --graph --all --decorate

# --- Limit Number of Commits ---
git log -n 5
git log -5  # shorthand

# --- Filter by Author ---
git log --author="John"

# --- Filter by Date ---
git log --since="2 weeks ago"
git log --after="2024-01-01" --before="2024-06-01"

# --- Filter by Message ---
git log --grep="fix"

# --- Show File Changes (stats) ---
git log --stat

# --- Show Actual Diff ---
git log -p
git log -p -1  # diff for the last commit only

# --- Show a Specific Commit ---
git show abc1234
git show HEAD
git show HEAD~2  # two commits back

# --- One-liner: Pretty Log (great alias candidate) ---
git log --oneline --graph --all --decorate --color
