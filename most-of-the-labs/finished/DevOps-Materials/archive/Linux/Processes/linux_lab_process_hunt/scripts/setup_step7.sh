#!/bin/bash
# Setup for Step 7: The last resort (kill -9)
# Start a process that IGNORES SIGTERM (stubborn process)

echo "Step 7 setup: Starting a stubborn dummy process..."

# Create a temporary script that ignores SIGTERM
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << 'EOF'
#!/bin/bash
# Dummy process that IGNORES SIGTERM (stubborn)

# Ignore SIGTERM - don't respond to gentle kill
trap '' SIGTERM

# Keep running indefinitely
while true; do
  sleep 1
done
EOF

chmod +x "$TEMP_SCRIPT"

# Start the stubborn process
"$TEMP_SCRIPT" &

DUMMY_PID=$!
echo "Started dummy_stubborn process (PID: $DUMMY_PID)"
echo "This process will IGNORE kill (SIGTERM) and requires kill -9."
exit 0
