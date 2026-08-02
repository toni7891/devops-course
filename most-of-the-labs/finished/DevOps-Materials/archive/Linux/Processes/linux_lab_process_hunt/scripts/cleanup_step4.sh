#!/bin/bash
# Cleanup for Step 4

echo "Step 4 cleanup: Stopping CPU-heavy processes..."

# Kill any infinite loops we started
pkill -f "while true" 2>/dev/null

sleep 1
echo "Cleanup complete."
exit 0
