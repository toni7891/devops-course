#!/bin/bash
# Topic: Init and First Commit
# Description: Creating a repository and making the first commit

# --- Create a New Project ---
mkdir demo-project
cd demo-project

# --- Initialize a Git Repository ---
git init

# Explore the .git directory
ls -la
ls -la .git

# --- The Full Lifecycle: Create → Add → Commit ---
# Create a file
echo "# My Project" > README.md

# Check the status (file is untracked)
git status

# Stage the file
git add README.md

# Check status again (file is staged)
git status

# Commit with a message
git commit -m "add README"

# View the commit
git log

# --- What Happens Without git init ---
cd /tmp
mkdir not-a-repo
cd not-a-repo
git status  # Error: not a git repository

# --- Delete .git to See What Happens ---
# cd back to demo-project
# rm -rf .git
# git status  # Error: no longer a repo (history is gone!)
