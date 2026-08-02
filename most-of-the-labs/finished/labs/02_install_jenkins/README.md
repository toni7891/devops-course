# Lab 02 — Install Jenkins via Docker

Corresponds to transcript chunk `02_Installing_Jenkins_and_UI_Tour.md`.

Files in this folder:

- [`Dockerfile`](Dockerfile) — Jenkins master image (jenkins/jenkins:lts-jdk17
  + blueocean, docker-plugin, git, workflow-aggregator, configuration-as-code, matrix-auth).
- [`plugins.txt`](plugins.txt) — plugin list installed via `jenkins-plugin-cli`.
- [`scripts/01_build_images.sh`](scripts/01_build_images.sh) — builds the master image and
  both agent images (agent Dockerfiles live in Lab 04's folder).
- [`scripts/02_network.sh`](scripts/02_network.sh) — creates the `jenkins-lab` Docker network.
- [`scripts/03_run.sh`](scripts/03_run.sh) — runs the master container.
- [`scripts/_session.sh`](scripts/_session.sh) — sourced by later labs' curl calls (login + CSRF crumb).

## Steps actually run

```bash
cd labs
bash 02_install_jenkins/scripts/01_build_images.sh
bash 02_install_jenkins/scripts/02_network.sh
bash 02_install_jenkins/scripts/03_run.sh
```

The run script publishes the Jenkins UI on **http://localhost:8081** (8080 was already taken by
another local container on this machine, so it's remapped — adjust if yours is free) and mounts:

- `/var/run/docker.sock` — so the docker-plugin cloud (Lab 04) can talk straight to the host's
  Docker daemon instead of the socat-proxy dance the video uses (functionally equivalent, no TLS
  cert plumbing needed for a local lab).
- `../04_agents_docker_cloud/jenkins.yaml` — Configuration-as-Code file that replaces the manual "unlock Jenkins /
  create first admin user / install suggested plugins" wizard from the video. Admin/admin is
  created automatically (`CASC_JENKINS_CONFIG` env var, set in the Dockerfile).
- `../repo` — the fixture git repo used by Labs 03 and 05, mounted read-only at `/repo`.

## Verification actually performed

```
$ curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/login
200

$ curl -s -u admin:admin http://localhost:8081/whoAmI/api/json
{"_class":"hudson.security.WhoAmI","anonymous":false,"authenticated":true,"name":"admin"}
```

Jenkins came up fully (`Jenkins is fully up and running` in the container logs), UI reachable,
admin/admin login works — no manual unlock-password step needed since CasC pre-provisions the
security realm.

## Note on one deviation from the video

The video proxies to Docker Desktop via an `alpine/socat` container and a manual TCP endpoint
(`tcp://<ip>:2375`) configured through the UI. That's necessary when Jenkins and Docker Desktop
are genuinely separate hosts. Here they're the same machine, so mounting `docker.sock` directly
is the simpler, equivalent path — same end result (Jenkins can launch containers on your local
Docker), less moving parts to keep working.
