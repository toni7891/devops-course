#!/bin/bash
# Cleanup for Step 6

echo "Step 6 cleanup: Stopping any remaining processes..."

# Clean up temp scripts and processes
pkill -f "dummy_normal" 2>/dev/null
pkill -f "mktemp" 2>/dev/null

sleep 1
echo "Cleanup complete."
exit 0
