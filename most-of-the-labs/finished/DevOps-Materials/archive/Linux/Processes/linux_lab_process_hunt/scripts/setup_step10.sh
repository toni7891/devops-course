#!/bin/bash
# Setup for Step 10: Synthesis & Challenge
# Start the most complex scenario with multiple processes, relationships, and signals

echo "Step 10 setup: Starting final challenge scenario..."

# Start legitimate background processes (2–3)
sleep 999 &
echo "  - Started legitimate process 1"

sleep 999 &
echo "  - Started legitimate process 2"

# Start a CPU hog (the main culprit)
(
  while true; do
    : # Burn CPU
  done
) &
echo "  - Started CPU-heavy culprit"

# Start a parent with children
(
  sleep 999 &  # Child
  sleep 999 &  # Child

  # Parent stays alive
  while true; do
    sleep 1
  done
) &
PARENT_PID=$!
echo "  - Started parent process ($PARENT_PID) with 2 children"

# Start a stubborn process (requires kill -9)
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << 'EOF'
#!/bin/bash
trap '' SIGTERM
while true; do sleep 1; done
EOF
chmod +x "$TEMP_SCRIPT"
"$TEMP_SCRIPT" &
echo "  - Started stubborn process (ignores SIGTERM)"

echo ""
echo "Scenario complexity: Multiple legitimate + problem processes, parent/child,"
echo "              CPU hogs, and signal-resistant processes."
echo "Challenge: Identify the problems and choose the right fix strategy."
exit 0
