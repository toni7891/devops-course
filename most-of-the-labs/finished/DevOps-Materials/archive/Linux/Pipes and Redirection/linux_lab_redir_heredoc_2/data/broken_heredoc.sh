#!/bin/bash
# Broken heredoc script - find and fix the 3 bugs!

# Bug 1: Space before closing delimiter
cat << EOF
This is some content
Line two of content
   EOF

# Bug 2: Undefined variable used
NAME="Alice"
cat << EOF
Hello, $NAME
Your score: $SCORE
EOF

# Bug 3: Wrong case for closing delimiter
cat << EOF
Final message here
eof
