#!/bin/bash
# Topic: Status and Add
# Description: Understanding the staging area and tracking file states

# --- Setup: Create a repo with some files ---
mkdir status-demo && cd status-demo
git init
echo "line 1" > file1.txt
echo "line 1" > file2.txt
echo "line 1" > file3.txt

# --- Check Status (all untracked) ---
git status

# --- Add a Single File ---
git add file1.txt
git status  # file1.txt is staged (green), others are untracked (red)

# --- Add Multiple Files ---
git add file2.txt file3.txt
git status  # all three are staged

# --- Commit All Staged Files ---
git commit -m "add initial files"

# --- Modify a Tracked File ---
echo "line 2" >> file1.txt
git status  # file1.txt is "modified" (red — unstaged)

# --- Stage the Modification ---
git add file1.txt
git status  # file1.txt changes are staged (green)

# --- Add All Changes at Once ---
echo "line 2" >> file2.txt
echo "line 2" >> file3.txt
git add .   # stages everything in current directory
git status

# --- Unstage a File ---
git restore --staged file3.txt
git status  # file3.txt is back to unstaged

# --- The Three Areas ---
# Working Directory: where you edit files
# Staging Area (Index): what will go into the next commit
# Repository (.git): committed snapshots
