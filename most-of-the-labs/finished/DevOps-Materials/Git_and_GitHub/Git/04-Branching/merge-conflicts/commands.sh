#!/bin/bash
# Topic: Merge Conflicts
# Description: Understanding and resolving merge conflicts

# --- Setup: Create a Conflict ---
# Start with a file on main
echo "Hello World" > greeting.txt
git add greeting.txt && git commit -m "add greeting"

# Create a branch and change the same line
git switch -c feature-a
echo "Hello from Feature A" > greeting.txt
git add greeting.txt && git commit -m "update greeting in feature-a"

# Go back to main and change the same line differently
git switch main
echo "Hello from Main" > greeting.txt
git add greeting.txt && git commit -m "update greeting in main"

# --- Trigger the Conflict ---
git merge feature-a
# Output: CONFLICT (content): Merge conflict in greeting.txt
# Automatic merge failed; fix conflicts and then commit the result.

# --- See the Conflict ---
git status
cat greeting.txt
# <<<<<<< HEAD
# Hello from Main
# =======
# Hello from Feature A
# >>>>>>> feature-a

# --- Resolve the Conflict ---
# Edit the file: choose one side, combine, or write something new
echo "Hello from Both Main and Feature A" > greeting.txt

# --- Complete the Merge ---
git add greeting.txt
git commit -m "merge feature-a: resolve greeting conflict"

# --- Verify ---
git log --oneline --graph --all

# --- Abort a Merge (if you want to start over) ---
# git merge --abort  # returns to pre-merge state
