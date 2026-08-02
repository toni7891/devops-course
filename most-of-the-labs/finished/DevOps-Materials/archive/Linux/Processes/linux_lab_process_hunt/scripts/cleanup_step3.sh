#!/bin/bash
# Cleanup for Step 3

echo "Step 3 cleanup: Stopping process hierarchy..."

# Kill any lingering sleep processes
pkill -f "sleep 999" 2>/dev/null

sleep 1
echo "Cleanup complete."
exit 0
