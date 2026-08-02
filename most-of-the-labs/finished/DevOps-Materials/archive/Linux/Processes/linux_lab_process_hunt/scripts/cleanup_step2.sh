#!/bin/bash
# Cleanup for Step 2: Kill all dummy processes started in setup

echo "Step 2 cleanup: Stopping dummy processes..."

# Kill any sleep processes started by setup_step2
pkill -f "sleep 999" 2>/dev/null

# Kill any dummy processes
pkill -f "dummy_process" 2>/dev/null

# Wait a moment for processes to terminate
sleep 1

echo "Cleanup complete."
exit 0
