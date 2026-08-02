#!/bin/bash
# Setup for Step 2: Filter processes by name
# Start a few background processes to search for

echo "Step 2 setup: Starting dummy processes..."

# Start some dummy processes in the background
for i in {1..3}; do
  sleep 999 &
done

# Start a distinctive dummy process
(while true; do echo "dummy_process running..."; sleep 1; done) &

echo "Started dummy processes. Use ps aux | grep to find them."
exit 0
