#!/bin/bash
PATHTOLOG="/tmp/runs.log"
WCLOG=$(wc -l /tmp/runs.log | awk '{ print $1 }')
RUNS=$(($WCLOG / 3 ))

echo "Running $(basename "$0")" >> /tmp/runs.log
echo "Logged to $PATHTOLOG" >> /tmp/runs.log
echo "This script has run $RUNS times." >> /tmp/runs.log
cat /tmp/runs.log | tail -n 3


