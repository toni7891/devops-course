#!/bin/bash
################################################################################
# Linux Scenario Lab: Managing a Shared Project Server - Cleanup Script
#
# Removes all resources created during the lab:
# - Users: dev1, dev2, ops1
# - Group: devteam
# - Directory: /opt/project
#
# Usage: sudo ./cleanup_lab.sh
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Scenario Lab: Cleanup                                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}This script must be run with sudo.${NC}"
    echo "  sudo ./cleanup_lab.sh"
    exit 1
fi

echo -e "${YELLOW}This will remove:${NC}"
echo "  - Users: dev1, dev2, ops1 (and their home directories)"
echo "  - Group: devteam"
echo "  - Directory: /opt/project"
echo ""
read -p "Are you sure? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo -e "${GREEN}[1/3] Removing users...${NC}"
for user in dev1 dev2 ops1; do
    if getent passwd "$user" >/dev/null 2>&1; then
        userdel -r "$user" 2>/dev/null || userdel "$user" 2>/dev/null || true
        echo "  Removed user: $user"
    else
        echo "  User $user does not exist - skipping"
    fi
done

echo -e "${GREEN}[2/3] Removing group...${NC}"
if getent group devteam >/dev/null 2>&1; then
    groupdel devteam 2>/dev/null || true
    echo "  Removed group: devteam"
else
    echo "  Group devteam does not exist - skipping"
fi

echo -e "${GREEN}[3/3] Removing project directory...${NC}"
if [ -d /opt/project ]; then
    rm -rf /opt/project
    echo "  Removed /opt/project"
else
    echo "  /opt/project does not exist - skipping"
fi

echo ""
echo -e "${GREEN}Cleanup complete!${NC}"
echo ""
