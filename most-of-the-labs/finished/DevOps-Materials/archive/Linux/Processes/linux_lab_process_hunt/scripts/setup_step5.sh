#!/bin/bash
# Setup for Step 5: First kill - graceful stopping
# Start a simple dummy process that can be killed

echo "Step 5 setup: Starting a dummy process to be killed..."

# Start a simple sleep process
sleep 999 &

DUMMY_PID=$!
echo "Started dummy process (PID: $DUMMY_PID)"
echo "Find it with: ps aux | grep sleep"
echo "Kill it with: kill $DUMMY_PID"
exit 0
