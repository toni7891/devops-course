#!/bin/bash
# Cleanup for Step 9

echo "Step 9 cleanup: Stopping all scenario processes..."

# Kill sleep processes
pkill -f "sleep 999" 2>/dev/null

# Kill CPU burners
pkill -f "while true" 2>/dev/null

# Force kill any stragglers
pkill -9 -f mktemp 2>/dev/null

sleep 1
echo "Cleanup complete."
exit 0
