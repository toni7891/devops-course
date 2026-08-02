#!/bin/bash
# This script logs 5 daily events to daily_log.txt
# BUG: Uses > instead of >> for all lines after the first
# As a result, each echo OVERWRITES the file — only EVENT 5 survives

echo "EVENT 1: $(date) - Morning system check: all services OK" > daily_log.txt
echo "EVENT 2: $(date) - Disk usage: $(df -h / | tail -1 | awk '{print $5}')" > daily_log.txt
echo "EVENT 3: $(date) - Active users: $(who | wc -l)" > daily_log.txt
echo "EVENT 4: $(date) - Memory free: $(free -h | grep Mem | awk '{print $4}')" > daily_log.txt
echo "EVENT 5: $(date) - Evening check: script complete" > daily_log.txt

echo ""
echo "Done. Check daily_log.txt"
