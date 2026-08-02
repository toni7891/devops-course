#!/bin/bash
# Cleanup for Step 5

echo "Step 5 cleanup: Stopping any remaining processes..."

pkill -f "sleep 999" 2>/dev/null

sleep 1
echo "Cleanup complete."
exit 0
