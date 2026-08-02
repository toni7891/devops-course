#!/usr/bin/env bash
set -euo pipefail
LABS_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# Generate the CasC file from its template, substituting this machine's absolute
# path to labs/repo (the docker-plugin bind-mounts it into every agent container,
# and the docker daemon only understands host paths).
sed "s|@LABS_REPO_HOST_PATH@|$LABS_DIR/repo|" \
  "$LABS_DIR/04_agents_docker_cloud/jenkins.yaml.template" \
  > "$LABS_DIR/04_agents_docker_cloud/jenkins.yaml"

docker rm -f jenkins-lab >/dev/null 2>&1 || true

docker run -d \
  --name jenkins-lab \
  --network jenkins-lab \
  --user root \
  -p 8081:8080 \
  -p 50000:50000 \
  -v jenkins-lab-home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$LABS_DIR/04_agents_docker_cloud/jenkins.yaml:/var/jenkins_home/casc/jenkins.yaml:ro" \
  -v "$LABS_DIR/repo:/repo:ro" \
  labs-jenkins-master:latest

echo "started jenkins-lab, waiting for it to come up on http://localhost:8081"
