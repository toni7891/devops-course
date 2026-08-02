#!/bin/bash
# Topic: What is Git?
# Description: Introduction to version control and Git basics

# --- Check Git Installation ---
git --version

# --- Quick Demo: Why Git Matters ---
# Create a project directory
mkdir my-first-project
cd my-first-project

# Initialize a Git repository
git init

# Create a file and track it
echo "Hello, World!" > hello.txt
git add hello.txt
git commit -m "initial commit"

# View the history
git log

# Make a change
echo "Hello, Git!" > hello.txt
git add hello.txt
git commit -m "update greeting"

# See both versions in history
git log --oneline

# Show we can go back in time
git diff HEAD~1 HEAD
