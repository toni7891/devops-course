#!/bin/bash
# Setup for Step 9: Real-world hunt
# Start a complex scenario with multiple processes of different types

echo "Step 9 setup: Starting real-world troubleshooting scenario..."

# Start a normal background process (legitimate)
sleep 999 &
echo "  - Started normal process (sleep 999)"

# Start a resource-heavy dummy process (the culprit)
(
  while true; do
    : # CPU burn
  done
) &
echo "  - Started resource-heavy process"

# Start a stubborn process that won't respond to SIGTERM
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << 'EOF'
#!/bin/bash
trap '' SIGTERM
while true; do sleep 1; done
EOF
chmod +x "$TEMP_SCRIPT"
"$TEMP_SCRIPT" &
echo "  - Started stubborn process"

echo ""
echo "Scenario: Multiple processes, one is resource-heavy, one ignores SIGTERM."
echo "Use top, ps, and grep to find the culprits."
exit 0
