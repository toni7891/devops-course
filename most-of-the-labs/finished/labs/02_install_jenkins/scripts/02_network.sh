#!/usr/bin/env bash
set -euo pipefail

docker network create jenkins-lab 2>/dev/null || echo "network jenkins-lab already exists"
docker network ls | grep jenkins-lab
