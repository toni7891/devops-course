#!/usr/bin/env bash
set -e

SUMMARY="coverage/coverage-summary.json"
THRESHOLD=70

if [ ! -f "$SUMMARY" ]; then
  echo "ERROR: $SUMMARY not found. Run npm test first."
  exit 1
fi

LINES=$(node -e "const s = require('./$SUMMARY'); console.log(s.total.lines.pct);")

echo "Lines coverage: ${LINES}%"

if (( $(echo "$LINES < $THRESHOLD" | bc -l) )); then
  echo "FAIL: coverage ${LINES}% is below threshold ${THRESHOLD}%"
  exit 1
fi

echo "PASS: coverage ${LINES}% meets threshold ${THRESHOLD}%"
