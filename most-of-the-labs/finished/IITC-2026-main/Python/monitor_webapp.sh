#!/bin/bash
# Script to monitor a running web server process
# Usage: ./monitor_webapp.sh <PROCESS_NAME>
# Example: ./monitor_webapp.sh uvicorn

PROCESS_NAME=${1:-"uvicorn"}

echo "=== Monitoring $PROCESS_NAME ==="
echo

# Find the process
PID=$(pgrep -f "$PROCESS_NAME" | head -1)

if [ -z "$PID" ]; then
    echo "Error: No process found matching '$PROCESS_NAME'"
    echo "Make sure your server is running first!"
    exit 1
fi

echo "Found process: $PID"
echo

# Show basic info
echo "--- Process Info ---"
ps -p $PID -o pid,ppid,%cpu,%mem,nlwp,comm

echo
echo "--- Open Files (first 10) ---"
lsof -p $PID 2>/dev/null | head -15

echo
echo "--- Network Connections ---"
lsof -i -p $PID 2>/dev/null | head -10

echo
echo "--- Monitoring CPU/Memory (press Ctrl+C to stop) ---"
echo "Updating every 2 seconds..."
pidstat -p $PID 2
