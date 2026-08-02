#!/bin/bash
################################################################################
#  Linux Lab 13 - ACL & Group Permissions Lab
#  Environment Setup Script
#
#  This script prepares the lab environment by creating users, groups, and
#  test files with the correct initial state for students to work through.
#
#  USAGE: sudo ./setup_environment.sh
#
################################################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=================================================================================${NC}"
echo -e "${YELLOW}    Linux Lab 13 - ACL & Group Permissions Lab${NC}"
echo -e "${YELLOW}    Environment Setup Script${NC}"
echo -e "${YELLOW}=================================================================================${NC}"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}ERROR: This script must be run as root (use sudo)${NC}"
   exit 1
fi

echo -e "${YELLOW}Step 1: Creating lab group 'superheroes'...${NC}"
if getent group superheroes > /dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Group 'superheroes' already exists${NC}"
else
    groupadd superheroes
    echo -e "${GREEN}  ✓ Created group 'superheroes'${NC}"
fi

echo ""
echo -e "${YELLOW}Step 2: Creating user 'batman'...${NC}"
if id batman > /dev/null 2>&1; then
    echo -e "${GREEN}  ✓ User 'batman' already exists${NC}"
else
    useradd -m -s /bin/bash batman || true
    # Lock the password to prevent login (students will use 'su' with sudo)
    usermod -L batman 2>/dev/null || true
    echo -e "${GREEN}  ✓ Created user 'batman'${NC}"
fi

echo ""
echo -e "${YELLOW}Step 3: Creating user 'superman'...${NC}"
if id superman > /dev/null 2>&1; then
    echo -e "${GREEN}  ✓ User 'superman' already exists${NC}"
else
    useradd -m -s /bin/bash superman || true
    # Lock the password
    usermod -L superman 2>/dev/null || true
    echo -e "${GREEN}  ✓ Created user 'superman'${NC}"
fi

echo ""
echo -e "${YELLOW}Step 4: Adding batman and superman to 'superheroes' group...${NC}"
usermod -aG superheroes batman
usermod -aG superheroes superman
echo -e "${GREEN}  ✓ Added batman to superheroes group${NC}"
echo -e "${GREEN}  ✓ Added superman to superheroes group${NC}"

echo ""
echo -e "${YELLOW}Step 5: Creating test file '/tmp/heroes.txt'...${NC}"
# Create the file with root ownership
cat > /tmp/heroes.txt << 'EOF'
Justice League Confidential File
Created for lab testing.
EOF

# Set initial permissions: 640 (owner rw, group r, others ---)
# This means batman and superman cannot access it yet (not in root group)
chmod 640 /tmp/heroes.txt
chown root:root /tmp/heroes.txt
echo -e "${GREEN}  ✓ Created /tmp/heroes.txt with permissions 640, owner root:root${NC}"

echo ""
echo -e "${YELLOW}Step 6: Verifying setup...${NC}"
echo ""

echo -e "${YELLOW}User 'batman':${NC}"
id batman || echo "Error verifying batman"

echo ""
echo -e "${YELLOW}User 'superman':${NC}"
id superman || echo "Error verifying superman"

echo ""
echo -e "${YELLOW}Group 'superheroes':${NC}"
getent group superheroes || echo "Error verifying group"

echo ""
echo -e "${YELLOW}File /tmp/heroes.txt:${NC}"
ls -l /tmp/heroes.txt || echo "Error verifying file"

echo ""
echo -e "${GREEN}=================================================================================${NC}"
echo -e "${GREEN}    Lab Environment Setup Complete!${NC}"
echo -e "${GREEN}=================================================================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Students should log out and back in (or run: newgrp superheroes)"
echo "  2. Open 'start_here.txt' to begin the lab"
echo "  3. Follow the 10 steps in order"
echo ""
echo "Note: Students will use 'su - batman' and 'su - superman' to test access"
echo "      (sudo allows password-less switching even though passwords are locked)"
echo ""
