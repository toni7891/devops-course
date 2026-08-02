# Lab 01 — Jenkins Theory (no hands-on steps)

Corresponds to transcript chunk `01_Introduction_and_Jenkins_Theory.md`.

This part of the course is conceptual — there is nothing to build or run yet.
It covers:

- What Jenkins is (automation platform: build/test/deploy via pipelines, or any scripted task).
- Master/agent infrastructure: the controller schedules builds, agents run them in their workspace.
- Two agent styles: **permanent agents** (static servers, SSH-connected) vs **cloud agents**
  (Docker/Kubernetes/EC2 Fleet — dynamically provisioned per build).
- Two job styles: **freestyle projects** (UI + shell steps) vs **pipelines** (Jenkinsfile,
  Groovy, staged: clone → build → test → package → deploy).

Everything from Lab 02 onward is the hands-on implementation of these concepts, built and
verified against a real local Jenkins + Docker environment.
