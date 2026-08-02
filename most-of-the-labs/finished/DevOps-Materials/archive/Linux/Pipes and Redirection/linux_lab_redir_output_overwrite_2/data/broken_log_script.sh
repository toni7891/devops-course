#!/bin/bash
# This script logs 5 system events to system_events.txt
# BUG: It uses > for every line, so only the last line survives

echo "EVENT 1: Script started at $(date)" > system_events.txt
echo "EVENT 2: User is $(whoami)" > system_events.txt
echo "EVENT 3: Running on host $(hostname)" > system_events.txt
echo "EVENT 4: Current directory is $(pwd)" > system_events.txt
echo "EVENT 5: Script finished at $(date)" > system_events.txt

echo ""
echo "Done! Check system_events.txt"
