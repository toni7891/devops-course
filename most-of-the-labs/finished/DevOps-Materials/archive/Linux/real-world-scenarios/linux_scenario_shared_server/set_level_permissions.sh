#!/bin/bash
################################################################################
# set_level_permissions.sh
#
# Creates the "broken" state that students must diagnose and fix in Level 2.
#
# The bugs introduced:
#   1. A dummy group called "it" is created
#   2. dev2 is added to the "it" group
#   3. dev2 is removed from the "devteam" group
#   4. /opt/project group ownership is set to "it" instead of "devteam"
#
# Students must fix this by:
#   - Discovering dev2 is in the wrong group (id dev2 / groups dev2)
#   - Removing dev2 from "it" and adding back to "devteam"
#   - Changing /opt/project group ownership back to devteam
#
# Run as root (sudo) after setup_environment.sh and after students have
# completed Level 1 (users and devteam group already exist).
#
# Usage: sudo ./set_level_permissions.sh
################################################################################

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR="/opt/project"

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}This script must be run with sudo.${NC}"
    echo "  sudo ./set_level_permissions.sh"
    exit 1
fi

if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}Error: $PROJECT_DIR does not exist.${NC}"
    echo "Run setup_environment.sh first."
    exit 1
fi

if ! id dev2 &>/dev/null; then
    echo -e "${RED}Error: user dev2 does not exist.${NC}"
    echo "Complete Level 1 first (create users and devteam group)."
    exit 1
fi

if ! getent group devteam &>/dev/null; then
    echo -e "${RED}Error: group devteam does not exist.${NC}"
    echo "Complete Level 1 first (create users and devteam group)."
    exit 1
fi

echo -e "${YELLOW}Setting broken state...${NC}"

# 1. Create dummy "it" group if it doesn't exist
if ! getent group it &>/dev/null; then
    groupadd it
    echo "  - Created group: it"
fi

# 2. Add dev2 to the "it" group
usermod -aG it dev2
echo "  - Added dev2 to group: it"

# 3. Remove dev2 from devteam (set their supplementary groups to only "it")
gpasswd -d dev2 devteam
echo "  - Removed dev2 from group: devteam"

echo ""
echo -e "${GREEN}Broken state applied:${NC}"
echo "  - Group 'it' created"
echo "  - dev2 is in group: it (NOT devteam)"
echo "  - dev2 removed from devteam"
echo ""
echo -e "${YELLOW}Students must diagnose why dev2 cannot collaborate with the team and fix it.${NC}"
