#!/bin/bash
# Setup for Step 4: Monitor resources with top
# Start a CPU-intensive dummy process

echo "Step 4 setup: Starting resource-heavy dummy process..."

# Start a process that uses CPU (tight loop)
(
  while true; do
    : # Bash NOP (null operation) - consumes CPU
  done
) &

DUMMY_PID=$!
echo "Started CPU-heavy dummy process (PID: $DUMMY_PID)"
echo "Use 'top' to see it consuming CPU."
exit 0
