#!/bin/bash
# Topic: .gitignore
# Description: Excluding files from version control

# --- Create a .gitignore File ---
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
vendor/
.venv/

# Environment variables (NEVER commit secrets)
.env
.env.local
.env.*.local

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Build output
dist/
build/
*.o
*.pyc
__pycache__/

# Logs
*.log
logs/

# Terraform
.terraform/
*.tfstate
*.tfstate.backup

# Docker
docker-compose.override.yml
EOF

# --- Stage and Commit .gitignore ---
git add .gitignore
git commit -m "add gitignore"

# --- Demo: gitignore in Action ---
mkdir node_modules
echo "big library" > node_modules/library.js
echo "SECRET_KEY=abc123" > .env
git status  # node_modules/ and .env should NOT appear

# --- Problem: File Already Tracked Before gitignore ---
echo "debug info" > debug.log
git add debug.log
git commit -m "add debug log"

# Now add *.log to .gitignore — but it is already tracked!
echo "*.log" >> .gitignore
git status  # debug.log still shows up when modified!

# Solution: remove from tracking (keeps the file on disk)
git rm --cached debug.log
git add .gitignore
git commit -m "stop tracking debug.log"

# --- Pattern Examples ---
# *.log          → ignore all .log files
# /TODO          → ignore TODO in root only
# build/         → ignore the build directory
# doc/*.txt      → ignore .txt in doc/ but not doc/sub/file.txt
# doc/**/*.pdf   → ignore .pdf in doc/ and all subdirectories
# !important.log → do NOT ignore this specific file (negate)
