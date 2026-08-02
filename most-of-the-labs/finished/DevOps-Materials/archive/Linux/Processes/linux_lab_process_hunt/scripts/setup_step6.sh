#!/bin/bash
# Setup for Step 6: Understanding SIGTERM
# Start a process that explicitly handles SIGTERM

echo "Step 6 setup: Starting a dummy process that handles SIGTERM..."

# Create a temporary script that handles SIGTERM
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << 'EOF'
#!/bin/bash
# Dummy process that handles SIGTERM gracefully

trap 'echo "[dummy_normal] Received SIGTERM, exiting cleanly..."; exit 0' SIGTERM

# Keep running
while true; do
  sleep 1
done
EOF

chmod +x "$TEMP_SCRIPT"

# Start the process
"$TEMP_SCRIPT" &

DUMMY_PID=$!
echo "Started dummy_normal process (PID: $DUMMY_PID)"
echo "This process will exit cleanly when it receives SIGTERM."
exit 0
