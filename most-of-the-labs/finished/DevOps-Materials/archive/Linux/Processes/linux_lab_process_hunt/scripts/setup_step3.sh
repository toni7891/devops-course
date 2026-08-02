#!/bin/bash
# Setup for Step 3: View parent/child process relationships
# Start a nested process hierarchy

echo "Step 3 setup: Starting process hierarchy..."

# Start a parent process that spawns children
(
  sleep 999 &  # Child 1
  sleep 999 &  # Child 2
  sleep 999    # Keep parent alive
) &

echo "Started parent process with children. Use pstree or ps auxf to see the tree."
exit 0
