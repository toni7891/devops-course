# Lab 04 — Agents & Docker Cloud

Corresponds to transcript chunks `16` through `22` (nodes & clouds, docker cloud config, agent
templates, running jobs on docker agents, poll SCM).

Instead of clicking through **Manage Jenkins → Nodes & Clouds → Configure Clouds → Add Docker**
as in the video, the whole cloud + both agent templates are declared once in
[`jenkins.yaml.template`](jenkins.yaml.template) (Configuration-as-Code) and applied automatically
on container boot. Same settings, same end state, reproducible from a text file instead of manual
UI clicks. Lab 02's `03_run.sh` renders the template into `jenkins.yaml` (gitignored), replacing
the `@LABS_REPO_HOST_PATH@` placeholder with this machine's absolute path to `labs/repo` — that
keeps the config portable across machines while giving the Docker daemon the real host path it
needs for the bind mount. Edit the template, not the generated file.

Agent images in this folder (built by Lab 02's `scripts/01_build_images.sh`):

- [`Dockerfile.agent-alpine`](Dockerfile.agent-alpine) — plain
  `jenkins/inbound-agent:alpine-jdk17`, label `docker-agent-alpine`. Mirrors the video's first,
  Python-less agent template.
- [`Dockerfile.agent-python`](Dockerfile.agent-python) — same base +
  `python3`/`pip`, label `docker-agent-python`. Mirrors the video's custom
  `devopsjourney1/myjenkinsagents:python` image.

## What the CasC config actually declares

- A Docker cloud (`unix:///var/run/docker.sock`) with `containerCap: 100`.
- Two templates, both using the **Attach** launcher (Jenkins `docker exec`s into the container to
  start the agent — no inbound JNLP networking needed) and `pullStrategy: PULL_NEVER` (use the
  locally-built image, don't try to pull from Docker Hub).
- The python template additionally bind-mounts the fixture repo into every spawned agent
  container: `mountsString: "type=bind,src=<host path to labs/repo>,dst=/repo"` — required so the
  freestyle/pipeline jobs can `git clone file:///repo` from *inside* the agent, not just the
  master.

## Verification actually performed

Triggered `my_first_job` (label `docker-agent-alpine`) and `my_python_job` (label
`docker-agent-python`) from Lab 03 and confirmed in the console output:

```
Building remotely on docker-0000butt6l00t on docker (docker-agent-alpine) ...
Building remotely on docker-0000c875cjodw on docker (docker-agent-python) ...
```

i.e. Jenkins actually spun up throwaway Docker containers per build, on the labelled image, ran
the job, then tore the container down (`DockerOnceRetentionStrategy`).

Independently confirmed the bind mount reaches the agent by racing a `docker ps` against a build
trigger and inspecting the live container:

```
docker inspect <container-id> --format '{{json .Mounts}}'
[...{"Type":"bind","Source":".../labs/repo","Destination":"/repo","RW":true}]
docker exec <container-id> ls -la /repo
drwxr-xr-x 12 jenkins jenkins  384 ... .git
-rw-r--r--  1 jenkins jenkins  855 ... Jenkinsfile
```

**Patience note**: on Apple Silicon the first build per agent label can sit queued for a minute or
so — the agent images run under amd64 emulation and the first container spawn is slow. The build
picks up on its own; don't start debugging labels like the instructor does in the video until it's
been stuck well past that.

## Bugs hit and fixed along the way

1. `dockerTemplateBase.volumesString` — CasC rejected it outright: `'volumesString' is deprecated`.
   Same for the newer-looking `volumes` list — also rejected: `'volumes' is deprecated`. Decompiled
   the installed `docker-plugin.jpi` (`javap` / `grep` on the class files) to find the
   CasC-blessed replacement: `mountsString`, format `type=bind,src=<host>,dst=<container>`. That's
   the one actually wired into container creation in this plugin version.
2. First few builds against `docker-agent-python` failed with `python3 hello_world.py: No such
   file` — turned out to be the same stale-job-config issue as Lab 03, not a cloud/mount problem.
