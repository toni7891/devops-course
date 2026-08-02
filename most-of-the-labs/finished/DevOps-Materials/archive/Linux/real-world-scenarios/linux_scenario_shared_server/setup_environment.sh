#!/bin/bash
################################################################################
# Linux Scenario Lab: Managing a Shared Project Server - Setup Script
#
# Creates a realistic project directory structure at /opt/project with:
# - Source code files (Python stubs)
# - Configuration files
# - Realistic log files (app.log, access.log, deploy.log)
# - Shell scripts
# - Documentation
#
# This script does NOT create users or groups - students do that themselves.
#
# Run as root (sudo) before students start the lab.
#
# Usage: sudo ./setup_environment.sh
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Scenario Lab: Managing a Shared Project Server - Setup   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}This script must be run with sudo.${NC}"
    echo "  sudo ./setup_environment.sh"
    exit 1
fi

PROJECT_DIR="/opt/project"

if [ -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}Warning: $PROJECT_DIR already exists.${NC}"
    echo -e "${YELLOW}Removing and recreating...${NC}"
    rm -rf "$PROJECT_DIR"
fi

echo -e "${GREEN}[1/6] Creating project directory structure...${NC}"
mkdir -p "$PROJECT_DIR"/{src,logs,config,backups,docs,scripts}

echo -e "${GREEN}[2/6] Creating source code files...${NC}"

cat > "$PROJECT_DIR/src/app.py" << 'PYEOF'
#!/usr/bin/env python3
"""Main application entry point - DevTeam Project Server."""

import logging
from config import load_config
from utils import setup_logging, check_health

def main():
    config = load_config()
    logger = setup_logging(config)

    logger.info("Server started on port %s", config['server']['port'])
    logger.info("Environment: %s", config['server']['environment'])

    # Main application loop
    while True:
        check_health(config)
        # ... handle requests ...

if __name__ == "__main__":
    main()
PYEOF

cat > "$PROJECT_DIR/src/config.py" << 'PYEOF'
#!/usr/bin/env python3
"""Configuration loader for the project server."""

import os
import configparser

def load_config(path="/opt/project/config/app.conf"):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def get_db_connection_string():
    config = load_config("/opt/project/config/db.conf")
    host = config.get('postgresql', 'host', fallback='localhost')
    port = config.get('postgresql', 'port', fallback='5432')
    db = config.get('postgresql', 'database', fallback='projectdb')
    return f"postgresql://{host}:{port}/{db}"
PYEOF

cat > "$PROJECT_DIR/src/utils.py" << 'PYEOF'
#!/usr/bin/env python3
"""Utility functions for the project server."""

import logging
import os

def setup_logging(config):
    log_file = config.get('logging', 'file', fallback='/opt/project/logs/app.log')
    log_level = config.get('logging', 'level', fallback='INFO')
    logging.basicConfig(filename=log_file, level=getattr(logging, log_level))
    return logging.getLogger(__name__)

def check_health(config):
    """Run health checks on all services."""
    checks = {
        'database': _check_db(config),
        'cache': _check_cache(config),
        'disk': _check_disk_space(),
    }
    return all(checks.values())

def _check_db(config):
    return True

def _check_cache(config):
    return True

def _check_disk_space(threshold=90):
    usage = os.statvfs('/')
    percent = (usage.f_blocks - usage.f_bfree) / usage.f_blocks * 100
    return percent < threshold
PYEOF

echo -e "${GREEN}[3/6] Creating configuration files...${NC}"

cat > "$PROJECT_DIR/config/app.conf" << 'CONFEOF'
[server]
host = 0.0.0.0
port = 8080
workers = 4
debug = false
environment = production

[database]
host = localhost
port = 5432
name = projectdb
user = app_user
# password stored in /etc/project/secrets - DO NOT commit passwords!

[cache]
host = localhost
port = 6379
ttl = 3600

[logging]
level = INFO
file = /opt/project/logs/app.log
max_size = 10MB
backup_count = 5
CONFEOF

cat > "$PROJECT_DIR/config/db.conf" << 'CONFEOF'
[postgresql]
host = localhost
port = 5432
database = projectdb
max_connections = 50
timeout = 30
ssl_mode = prefer

[backup]
schedule = daily
retention_days = 30
backup_dir = /opt/project/backups
CONFEOF

cat > "$PROJECT_DIR/config/nginx.conf" << 'CONFEOF'
server {
    listen 80;
    server_name project.company.local;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8080/api/;
        proxy_read_timeout 60s;
    }

    location /static/ {
        alias /opt/project/static/;
        expires 30d;
    }

    access_log /opt/project/logs/access.log;
    error_log /opt/project/logs/error.log;
}
CONFEOF

echo -e "${GREEN}[4/6] Creating shell scripts...${NC}"

cat > "$PROJECT_DIR/scripts/deploy.sh" << 'SHEOF'
#!/bin/bash
# Deployment script for the project
# Usage: ./deploy.sh <version>
set -e

VERSION="${1:?Usage: ./deploy.sh <version>}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG="/opt/project/logs/deploy.log"

echo "$TIMESTAMP | $VERSION | STARTED | $USER | Deployment started" >> "$LOG"

echo "Pulling version $VERSION..."
echo "Running tests..."
echo "Restarting services..."

echo "$TIMESTAMP | $VERSION | SUCCESS | $USER | Deployment completed" >> "$LOG"
echo "Deployment of $VERSION completed successfully."
SHEOF

cat > "$PROJECT_DIR/scripts/backup.sh" << 'SHEOF'
#!/bin/bash
# Backup script for the project database and files
# Usage: ./backup.sh
set -e

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_DIR="/opt/project/backups"
BACKUP_FILE="$BACKUP_DIR/backup_${TIMESTAMP}.tar.gz"

echo "[$(date)] Starting backup..."
tar -czf "$BACKUP_FILE" /opt/project/src /opt/project/config 2>/dev/null || true
echo "[$(date)] Backup saved to $BACKUP_FILE"
SHEOF

cat > "$PROJECT_DIR/scripts/health_check.sh" << 'SHEOF'
#!/bin/bash
# Health check script - monitors server status
# Usage: ./health_check.sh

echo "=== Health Check Report ==="
echo "Date: $(date)"
echo ""
echo "--- System ---"
echo "Uptime: $(uptime -p 2>/dev/null || echo 'N/A')"
echo "Load: $(cat /proc/loadavg 2>/dev/null || echo 'N/A')"
echo ""
echo "--- Disk ---"
df -h /opt/project 2>/dev/null || echo "N/A"
echo ""
echo "--- Services ---"
echo "App server: checking port 8080..."
ss -tlnp 2>/dev/null | grep 8080 || echo "  Not running"
echo ""
echo "=== End Report ==="
SHEOF

chmod +x "$PROJECT_DIR/scripts/"*.sh

echo -e "${GREEN}[5/6] Generating realistic log files...${NC}"

# ──────────────────────────────────────────────────────────────────────────────
# app.log - Application log (~65 lines)
# ──────────────────────────────────────────────────────────────────────────────
cat > "$PROJECT_DIR/logs/app.log" << 'LOGEOF'
2024-01-15 07:00:01 INFO  Server startup initiated - loading configuration
2024-01-15 07:00:02 INFO  Configuration loaded from /opt/project/config/app.conf
2024-01-15 07:00:03 INFO  Database connection established to localhost:5432
2024-01-15 07:00:03 INFO  Cache connection established to localhost:6379
2024-01-15 07:00:04 INFO  Server started on port 8080 - ready to accept connections
2024-01-15 07:05:00 INFO  Health check passed - all services operational
2024-01-15 07:15:22 INFO  user dev1 logged in from 192.168.1.10
2024-01-15 07:16:01 INFO  GET /dashboard served to 192.168.1.10 in 45ms
2024-01-15 07:30:00 INFO  Health check passed - all services operational
2024-01-15 07:45:11 WARN  High memory usage detected: 78%
2024-01-15 08:00:00 INFO  Health check passed - all services operational
2024-01-15 08:02:33 INFO  user dev2 logged in from 192.168.1.11
2024-01-15 08:03:15 INFO  POST /api/deploy received from 192.168.1.11
2024-01-15 08:03:18 ERROR Deploy failed for version v1.2.1 - unit tests did not pass
2024-01-15 08:03:19 WARN  Rollback initiated for failed deployment v1.2.1
2024-01-15 08:03:25 INFO  Rollback completed successfully - server running v1.2.0
2024-01-15 08:15:00 WARN  High memory usage detected: 82%
2024-01-15 08:30:00 INFO  Health check passed - all services operational
2024-01-15 08:45:07 INFO  user ops1 logged in from 192.168.1.50
2024-01-15 08:45:30 INFO  ops1 executed health_check.sh - all services nominal
2024-01-15 08:50:12 ERROR Connection refused from cache server localhost:6379
2024-01-15 08:50:13 WARN  Cache unavailable - falling back to direct database queries
2024-01-15 08:50:14 WARN  Response time degraded: average 850ms (threshold: 500ms)
2024-01-15 08:51:00 INFO  Cache server reconnected successfully
2024-01-15 08:51:01 INFO  Response times normalized - average 45ms
2024-01-15 09:00:00 INFO  Health check passed - all services operational
2024-01-15 09:10:44 INFO  user dev1 logged in from 192.168.1.10
2024-01-15 09:11:02 INFO  GET /api/users served to 192.168.1.10 in 32ms
2024-01-15 09:15:33 ERROR Authentication failed for user admin from 203.0.113.42
2024-01-15 09:15:34 WARN  Suspicious login attempt from external IP 203.0.113.42
2024-01-15 09:15:35 ERROR Authentication failed for user admin from 203.0.113.42
2024-01-15 09:15:36 ERROR Authentication failed for user root from 203.0.113.42
2024-01-15 09:15:37 WARN  Multiple failed login attempts from 203.0.113.42 - blocking IP
2024-01-15 09:30:00 INFO  Health check passed - all services operational
2024-01-15 09:45:22 INFO  Scheduled backup started
2024-01-15 09:46:15 INFO  Scheduled backup completed - 2.3GB saved to /opt/project/backups
2024-01-15 10:00:00 INFO  Health check passed - all services operational
2024-01-15 10:10:05 WARN  Disk space usage at 75% on /opt partition
2024-01-15 10:30:00 INFO  Health check passed - all services operational
2024-01-15 10:45:18 INFO  user dev2 logged in from 192.168.1.11
2024-01-15 10:46:00 INFO  POST /api/deploy received from 192.168.1.11
2024-01-15 10:46:30 INFO  Deploy v1.2.2 completed successfully
2024-01-15 10:46:31 INFO  Server restarted with version v1.2.2
2024-01-15 11:00:00 INFO  Health check passed - all services operational
2024-01-15 11:15:09 WARN  High memory usage detected: 85%
2024-01-15 11:15:10 WARN  Initiating garbage collection cycle
2024-01-15 11:15:12 INFO  Garbage collection completed - memory usage at 52%
2024-01-15 11:30:00 INFO  Health check passed - all services operational
2024-01-15 11:45:33 ERROR Database query timeout after 30s - query: SELECT * FROM audit_logs
2024-01-15 11:45:34 WARN  Slow query detected - recommending index on audit_logs.created_at
2024-01-15 12:00:00 INFO  Health check passed - all services operational
2024-01-15 12:30:00 INFO  Health check passed - all services operational
2024-01-15 13:00:00 INFO  Health check passed - all services operational
2024-01-15 13:05:44 INFO  user ops1 logged in from 192.168.1.50
2024-01-15 13:06:00 INFO  ops1 executed backup.sh manually
2024-01-15 13:06:45 INFO  Manual backup completed - 2.3GB saved
2024-01-15 13:30:00 INFO  Health check passed - all services operational
2024-01-15 14:00:00 INFO  Health check passed - all services operational
2024-01-15 14:15:22 ERROR Connection timeout to database localhost:5432
2024-01-15 14:15:23 ERROR Database connection lost - attempting reconnect
2024-01-15 14:15:25 WARN  Database reconnect attempt 1 of 5
2024-01-15 14:15:30 INFO  Database connection re-established successfully
2024-01-15 14:30:00 INFO  Health check passed - all services operational
2024-01-15 15:00:00 INFO  Health check passed - all services operational
2024-01-15 15:30:00 INFO  Health check passed - all services operational
2024-01-15 15:45:10 WARN  Disk space usage at 80% on /opt partition
2024-01-15 16:00:00 INFO  Health check passed - all services operational
2024-01-15 16:30:00 INFO  Health check passed - all services operational
2024-01-15 16:45:00 INFO  Log rotation triggered - archiving logs older than 7 days
2024-01-15 16:45:05 INFO  Log rotation completed - 3 files archived
LOGEOF

# ──────────────────────────────────────────────────────────────────────────────
# access.log - Web access log (~45 lines)
# ──────────────────────────────────────────────────────────────────────────────
cat > "$PROJECT_DIR/logs/access.log" << 'LOGEOF'
192.168.1.10 GET /index.html 200 3421
192.168.1.10 GET /static/style.css 200 1205
192.168.1.10 POST /login 200 512
192.168.1.10 GET /dashboard 200 8732
192.168.1.11 GET /index.html 200 3421
192.168.1.11 POST /login 200 512
192.168.1.11 GET /dashboard 200 8732
192.168.1.11 POST /api/deploy 200 1024
192.168.1.50 GET /index.html 200 3421
192.168.1.50 POST /login 200 512
192.168.1.50 GET /dashboard 200 8732
192.168.1.50 GET /api/health 200 256
203.0.113.42 POST /login 401 128
203.0.113.42 POST /login 401 128
203.0.113.42 POST /login 401 128
203.0.113.42 GET /admin 404 0
203.0.113.42 GET /wp-admin 404 0
203.0.113.42 GET /phpmyadmin 404 0
203.0.113.42 GET /.env 404 0
192.168.1.10 GET /api/users 200 4096
192.168.1.10 GET /api/orders 200 2048
192.168.1.11 GET /api/users 200 4096
192.168.1.11 POST /api/deploy 500 256
192.168.1.11 POST /api/deploy 200 1024
192.168.1.50 GET /api/health 200 256
192.168.1.50 GET /api/logs 200 8192
192.168.1.10 GET /dashboard 200 8732
192.168.1.10 GET /static/app.js 200 15360
192.168.1.10 GET /api/status 200 512
192.168.1.30 GET /index.html 200 3421
192.168.1.30 GET /about 200 2048
192.168.1.30 POST /login 200 512
192.168.1.30 GET /dashboard 200 8732
192.168.1.11 GET /api/users 200 4096
192.168.1.11 PUT /api/users/42 200 512
192.168.1.50 GET /api/health 200 256
10.0.0.5 GET /api/internal/sync 200 1024
10.0.0.5 GET /api/internal/sync 200 1024
192.168.1.10 GET /dashboard 200 8732
192.168.1.10 POST /api/orders 201 512
192.168.1.10 GET /api/orders/4021 200 1024
192.168.1.50 POST /api/backup 200 256
192.168.1.50 GET /api/health 200 256
203.0.113.99 GET /robots.txt 200 64
203.0.113.99 GET /sitemap.xml 404 0
LOGEOF

# ──────────────────────────────────────────────────────────────────────────────
# deploy.log - Deployment history (~20 lines)
# ──────────────────────────────────────────────────────────────────────────────
cat > "$PROJECT_DIR/logs/deploy.log" << 'LOGEOF'
2024-01-02 09:00:00 | v1.0.0 | SUCCESS | ops1  | Initial production deployment
2024-01-03 14:30:00 | v1.0.1 | SUCCESS | dev1  | Hotfix: login page CSS
2024-01-05 10:15:00 | v1.0.2 | SUCCESS | dev2  | Feature: user profile page
2024-01-06 11:00:00 | v1.0.3 | FAILED  | dev2  | Build error: missing dependency
2024-01-06 14:00:00 | v1.0.3 | SUCCESS | dev2  | Fixed dependency and redeployed
2024-01-08 09:30:00 | v1.1.0 | SUCCESS | ops1  | Major update: API v2 endpoints
2024-01-09 16:00:00 | v1.1.1 | FAILED  | dev1  | Test failure: payment module
2024-01-10 09:00:00 | v1.1.1 | SUCCESS | dev1  | Fixed payment tests and redeployed
2024-01-11 13:45:00 | v1.1.2 | SUCCESS | dev2  | Feature: order tracking
2024-01-12 10:00:00 | v1.1.3 | SUCCESS | ops1  | Security patch: update dependencies
2024-01-12 15:30:00 | v1.1.4 | FAILED  | dev1  | Rollback: database migration error
2024-01-13 09:00:00 | v1.1.4 | SUCCESS | ops1  | Fixed migration and redeployed
2024-01-14 11:00:00 | v1.2.0 | SUCCESS | dev1  | Major: new dashboard UI
2024-01-14 16:30:00 | v1.2.0 | SUCCESS | ops1  | Config update: increased workers to 4
2024-01-15 08:03:18 | v1.2.1 | FAILED  | dev2  | Unit tests did not pass
2024-01-15 10:46:30 | v1.2.2 | SUCCESS | dev2  | Bug fixes and test corrections
LOGEOF

echo -e "${GREEN}[6/6] Creating documentation and remaining files...${NC}"

cat > "$PROJECT_DIR/docs/README.md" << 'DOCEOF'
# Project Server Documentation

## Overview
Internal web application server for the development team.

## Architecture
- **Application**: Python (Flask) running on port 8080
- **Database**: PostgreSQL on port 5432
- **Cache**: Redis on port 6379
- **Reverse Proxy**: Nginx on port 80

## Directory Structure
- `src/` - Application source code
- `logs/` - Application and access logs
- `config/` - Configuration files
- `scripts/` - Operational scripts (deploy, backup, health check)
- `backups/` - Database and file backups
- `docs/` - This documentation

## Team
- dev1, dev2 - Developers
- ops1 - DevOps Engineer

## Deployment
Use `scripts/deploy.sh <version>` to deploy a new version.

## Monitoring
Use `scripts/health_check.sh` to run a health check.
DOCEOF

# Create a placeholder backup file
touch "$PROJECT_DIR/backups/backup_2024-01-14.tar.gz"

# Set initial permissions - root:root, standard permissions
# Students will change these during the lab
chown -R root:root "$PROJECT_DIR"
chmod 755 "$PROJECT_DIR"
find "$PROJECT_DIR" -type d -exec chmod 755 {} \;
find "$PROJECT_DIR" -type f -exec chmod 644 {} \;
chmod +x "$PROJECT_DIR/scripts/"*.sh
chmod +x "$PROJECT_DIR/src/"*.py

echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo -e "${BLUE}Summary:${NC}"
echo "  - Created $PROJECT_DIR/ with full project structure"
echo "  - Source code:    src/app.py, config.py, utils.py"
echo "  - Config files:   config/app.conf, db.conf, nginx.conf"
echo "  - Log files:      logs/app.log (65 lines), access.log (45 lines), deploy.log (16 lines)"
echo "  - Scripts:        scripts/deploy.sh, backup.sh, health_check.sh"
echo "  - Documentation:  docs/README.md"
echo ""
echo -e "${BLUE}What students will do:${NC}"
echo "  - Create users: dev1, dev2, ops1"
echo "  - Create group: devteam"
echo "  - Set ownership and permissions on $PROJECT_DIR"
echo "  - Analyze log files with grep, pipes, and redirection"
echo ""
echo -e "${YELLOW}Note: Users and groups are NOT created by this script.${NC}"
echo -e "${YELLOW}Students must create them as part of the lab exercises.${NC}"
echo ""
