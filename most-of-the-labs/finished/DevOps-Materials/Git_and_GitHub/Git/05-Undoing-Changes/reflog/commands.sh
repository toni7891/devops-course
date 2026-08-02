#!/bin/bash
# Topic: Git Reflog
# Description: The safety net — recovering lost commits

# --- View the Reflog ---
git reflog
# Shows every time HEAD moved: commits, checkouts, resets, merges, rebases

# --- Example Output ---
# abc1234 HEAD@{0}: commit: add feature
# def5678 HEAD@{1}: checkout: moving from main to feature
# 789abcd HEAD@{2}: reset: moving to HEAD~2
# ...

# --- Recovery Scenario: Accidentally Reset --hard ---
git log --oneline  # 3 commits
git reset --hard HEAD~2  # oops! lost 2 commits
git log --oneline  # only 1 commit

# Find the lost commit
git reflog

# Recover by resetting back to it
git reset --hard HEAD@{1}  # or use the hash
git log --oneline  # commits are back!

# --- Recovery Scenario: Create a Branch from Lost Commit ---
git reflog
git branch recovered-work abc1234  # create a branch pointing to the lost commit
git switch recovered-work

# --- Reflog Expiry ---
# Entries expire after 90 days (default)
# Unreachable entries expire after 30 days
git reflog expire --expire=now --all  # force expire (don't run this normally!)
