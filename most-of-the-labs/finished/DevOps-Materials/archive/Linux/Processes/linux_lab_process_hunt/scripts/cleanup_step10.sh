#!/bin/bash
# Cleanup for Step 10 (Final)

echo "Step 10 cleanup: Final cleanup - removing all test processes..."

# Kill all our test processes with prejudice
pkill -f "sleep 999" 2>/dev/null
pkill -f "while true" 2>/dev/null
pkill -9 -f mktemp 2>/dev/null

sleep 1
echo "Cleanup complete. Lab finished!"
exit 0
