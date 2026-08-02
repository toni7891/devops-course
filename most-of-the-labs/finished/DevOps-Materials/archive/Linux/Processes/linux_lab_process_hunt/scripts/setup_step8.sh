#!/bin/bash
# Setup for Step 8: Multiple processes - parent/child family
# Start a parent with multiple children

echo "Step 8 setup: Starting parent process with children..."

# Start a parent process that spawns children
(
  echo "[parent] Starting with 3 children..."

  sleep 999 &  # Child 1
  sleep 999 &  # Child 2
  sleep 999 &  # Child 3

  # Keep parent alive
  while true; do
    sleep 1
  done
) &

PARENT_PID=$!
echo "Started parent process (PID: $PARENT_PID) with 3 children."
echo "Use 'ps auxf | grep -A 5 $$' to see the family tree."
exit 0
