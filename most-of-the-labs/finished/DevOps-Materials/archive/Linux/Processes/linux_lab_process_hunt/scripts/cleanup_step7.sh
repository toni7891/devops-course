#!/bin/bash
# Cleanup for Step 7

echo "Step 7 cleanup: Force-killing any remaining processes..."

# Force kill any stubborn processes
pkill -9 -f "dummy_stubborn" 2>/dev/null

sleep 1
echo "Cleanup complete."
exit 0
