#!/usr/bin/env bash
set -euo pipefail
LABS_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

docker build -t labs-jenkins-master:latest \
  -f "$LABS_DIR/02_install_jenkins/Dockerfile" "$LABS_DIR/02_install_jenkins"

# Agent images are a Lab 04 topic but get built up front so one script preps everything.
# --platform linux/amd64: jenkins/inbound-agent alpine tags publish no arm64 manifest,
# so on Apple Silicon they must build/run under amd64 emulation.
docker build --platform linux/amd64 -t labs-agent-alpine:latest \
  -f "$LABS_DIR/04_agents_docker_cloud/Dockerfile.agent-alpine" "$LABS_DIR/04_agents_docker_cloud"
docker build --platform linux/amd64 -t labs-agent-python:latest \
  -f "$LABS_DIR/04_agents_docker_cloud/Dockerfile.agent-python" "$LABS_DIR/04_agents_docker_cloud"
