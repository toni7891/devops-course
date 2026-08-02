#!/bin/bash
# Cleanup for Step 8

echo "Step 8 cleanup: Stopping parent and children processes..."

# Kill any sleep and parent processes
pkill -f "sleep 999" 2>/dev/null
pkill -f "while true" 2>/dev/null

sleep 1
echo "Cleanup complete."
exit 0
