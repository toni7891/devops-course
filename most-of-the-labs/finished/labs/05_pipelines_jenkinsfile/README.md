# Lab 05 — Pipelines & Jenkinsfile

Corresponds to transcript chunks `23` through `28` (pipeline intro, Jenkinsfile syntax, running
and debugging stages, Jenkinsfile-from-SCM, building out build/test/deliver with the real app).

- [`my_first_build_pipeline.xml`](my_first_build_pipeline.xml) (in this folder) — a
  `WorkflowJob`/`CpsScmFlowDefinition` pointing at `file:///repo`, script path `Jenkinsfile`. This
  is the "Pipeline script from SCM" mode from the video, not the inline-script mode — created
  directly rather than starting inline and migrating, since the end state is the same.
- [`../repo/Jenkinsfile`](../repo/Jenkinsfile) — declarative pipeline, agent label
  `docker-agent-python`, `pollSCM('* * * * *')`, three stages: Build (`pip install`), Test
  (`python3 hello.py` twice, once with `--name=Brad`), Deliver (placeholder echo). Content matches
  the instructor's real `jenkins-101-master/Jenkinsfile`, with one adjustment noted below. It lives
  in `../repo/` rather than here because the whole point of "pipeline script from SCM" is that the
  Jenkinsfile ships inside the source repository.
- [`../repo/myapp/hello.py`](../repo/myapp/hello.py), `myapp/requirements.txt` — the Python "fire"
  CLI app the pipeline builds and tests.

## Steps actually run

```bash
cd labs
source 02_install_jenkins/scripts/_session.sh
curl -b "$COOKIE_JAR" -u "$AUTH" -H "$CRUMB_HEADER" -H "Content-Type: application/xml" \
  --data-binary @05_pipelines_jenkinsfile/my_first_build_pipeline.xml \
  "$JENKINS_URL/createItem?name=my_first_build_pipeline"
curl -b "$COOKIE_JAR" -u "$AUTH" -H "$CRUMB_HEADER" -X POST \
  "$JENKINS_URL/job/my_first_build_pipeline/build"
```

## Verification actually performed — final green run

```
Obtained Jenkinsfile from git file:///repo
Running on docker-0000cg3omz1v9 on docker in /home/jenkins/agent/workspace/my_first_build_pipeline
[Pipeline] { (Build)     -> pip install --break-system-packages -r requirements.txt  -> OK
[Pipeline] { (Test)      -> python3 hello.py            -> Hello World!
                          -> python3 hello.py --name=Brad -> Hello Brad!
[Pipeline] { (Deliver)   -> echo "doing delivery stuff.." -> OK
Finished: SUCCESS
```

Blue Ocean's node API confirms all three stages green (see Lab 06). A later build also fired on
its own — `Started by an SCM change` — because of the `pollSCM('* * * * *')` trigger picking up a
new commit, exactly like the auto-trigger behavior demoed in the video.

## Bugs hit and fixed along the way

1. **Master couldn't read the Jenkinsfile from `/repo`**: `fatal: detected dubious ownership in
   repository at '/repo/.git'`. The master container runs as root (`--user root`, needed for
   `docker.sock` access) but the bind-mounted repo is owned by the host user, so git 2.54's
   ownership check refused it. Fixed by adding `git config --system --add safe.directory '*'` to
   the master `Dockerfile` — a deliberate wildcard since this is a disposable lab container, not
   something to do on a real shared Jenkins master.
2. **`fire==0.4.0` (the version pinned in the instructor's original repo) crashed on Test**:
   `ModuleNotFoundError: No module named 'pipes'`. Our agent image installs whatever `python3` apk
   currently ships (3.14), and the stdlib `pipes` module — deprecated since 3.11 — was removed in
   3.13. `fire` didn't drop its `pipes` import until later releases. Confirmed by pulling
   `fire`'s `core.py` from GitHub across versions: 0.6.0 still imports `pipes`; 0.7.1 uses `shlex`
   instead. Bumped `myapp/requirements.txt` to `fire==0.7.1` and reran — passed.
