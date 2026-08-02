#!/bin/bash
# Topic: Git Stash
# Description: Temporarily shelving uncommitted changes

# --- Setup: Working on a Feature ---
echo "work in progress" >> feature.txt
git status  # modified, not committed

# --- Stash the Changes ---
git stash
git status  # clean working directory
cat feature.txt  # changes are gone (safely stored)

# --- List Stashes ---
git stash list
# stash@{0}: WIP on main: abc1234 last commit message

# --- Restore Stashed Changes ---
git stash pop    # restores AND removes from stash list
# or:
git stash apply  # restores but KEEPS in stash list

# --- Stash with a Message ---
git stash push -m "work in progress: user authentication"
git stash list  # now shows the custom message

# --- Stash Specific Files ---
git stash push -m "stash only config" config.yaml

# --- View Stash Contents ---
git stash show           # summary of changes
git stash show -p        # full diff
git stash show stash@{1} # view a specific stash

# --- Drop a Specific Stash ---
git stash drop stash@{0}

# --- Clear All Stashes ---
git stash clear  # WARNING: removes all stashes

# --- Create a Branch from Stash ---
git stash branch new-feature stash@{0}
# Creates a new branch, checks it out, and applies the stash
