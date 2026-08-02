# Jenkins Course Labs

Hands-on labs for each topic in `transcript_chunks/`, actually built and run end-to-end against a
real local Jenkins (Docker) + Docker Cloud agent setup — not just written instructions.

## Layout

```
labs/
  01_intro_theory/
    README.md                     theory only — nothing to run
  02_install_jenkins/
    README.md
    Dockerfile                    Jenkins master image
    plugins.txt                   plugins baked into the master
    scripts/01_build_images.sh    builds master + both agent images
    scripts/02_network.sh         creates the jenkins-lab docker network
    scripts/03_run.sh             runs the master container
    scripts/_session.sh           auth/crumb helper for the curl calls in later labs
  03_freestyle_projects/
    README.md
    my_first_job.xml              freestyle job: hello world + env vars
    my_python_job.xml             freestyle job: clone repo, run helloworld.py
  04_agents_docker_cloud/
    README.md
    Dockerfile.agent-alpine       plain agent image (label docker-agent-alpine)
    Dockerfile.agent-python       agent image with python3/pip (label docker-agent-python)
    jenkins.yaml.template         Configuration-as-Code: admin user + docker cloud + templates
                                  (03_run.sh generates jenkins.yaml from it, substituting this
                                  machine's absolute path to repo/ — the generated file is
                                  gitignored, edit the template)
  05_pipelines_jenkinsfile/
    README.md
    my_first_build_pipeline.xml   pipeline job pointing at repo/Jenkinsfile
  06_blue_ocean/
    README.md

  repo/       fixture git repo the jobs clone from (file:///repo) — shared across labs 03/05
```

Each numbered folder's README explains that lab's slice of the transcript and includes the actual
verified output from running it — not just what's supposed to happen. The only shared piece is
`repo/`, since one git fixture serves both the freestyle and pipeline jobs.

The `repo/` fixture is synced from `jenkins-101-master/` at the repo root, which is the
instructor's real companion repo for this course (added after the labs were first scaffolded) —
`myapp/hello.py`, `helloworld.py`, and `Jenkinsfile` all match that source, with two intentional
deviations documented in Lab 05's README (a `pipes`-module Python compat fix and a git
safe-directory fix), both being environment quirks of running this in 2026 rather than mistakes in
the original material.

## Platform support

- **macOS** — fully verified end-to-end (Apple Silicon; agent images run under amd64 emulation,
  which makes the *first* build per agent label slow — see Lab 04's patience note).
- **Linux** — fully verified end-to-end on a fresh Ubuntu 24.04 amd64 EC2 instance
  (`docker.io` from apt, nothing preinstalled): image builds, container boot with CasC, both
  freestyle jobs, the pipeline (all stages green), and Blue Ocean all passed unmodified. On amd64
  the `--platform linux/amd64` flags are no-ops and agents run native.
- **Windows** — run everything inside **WSL2** (with Docker Desktop's WSL integration enabled)
  and it behaves exactly like the Linux case: bash, `python3`, and the `/var/run/docker.sock`
  mount all work there. The scripts are not written for PowerShell/cmd, and plain Git Bash is
  hit-or-miss (path mangling, no python3) — WSL2 is the supported route.

Nothing is machine-specific: the one absolute host path the setup needs (the docker-plugin
bind-mounts `repo/` into agent containers, and the Docker daemon only understands host paths) is
substituted into the CasC config at `03_run.sh` time from wherever you cloned the repo.

## Running it yourself

```bash
cd labs
bash 02_install_jenkins/scripts/01_build_images.sh
bash 02_install_jenkins/scripts/02_network.sh
bash 02_install_jenkins/scripts/03_run.sh
# wait for http://localhost:8081/login to return 200, then:
source 02_install_jenkins/scripts/_session.sh   # sets $JENKINS_URL, $AUTH, $COOKIE_JAR, $CRUMB_HEADER
```

From there, each lab README shows the exact `curl` calls used to create/trigger its job(s).

## What's verified, end to end

- **Lab 02**: image builds, network, container boots, CasC applies (admin/admin, no manual unlock).
- **Lab 03**: both freestyle jobs built successfully on real docker agents.
- **Lab 04**: Docker cloud + both agent templates provisioned real, throwaway containers per build.
- **Lab 05**: full declarative pipeline (Build/Test/Deliver) green, including the fixture repo's
  fire-based CLI app; pollSCM auto-triggered a build on a new commit, unprompted.
- **Lab 06**: Blue Ocean REST API confirms the same three green stages.

## Cleaning up

```bash
docker rm -f jenkins-lab
docker volume rm jenkins-lab-home   # only if you want to wipe all job history/config too
docker network rm jenkins-lab
```

The lab container (`jenkins-lab`) is currently left running on `http://localhost:8081` — stop/remove
it with the above whenever you're done poking at it.
