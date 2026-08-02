# Lab 03 — Freestyle Projects

Corresponds to transcript chunks `11` through `15` (first freestyle job, env vars, workspace,
file system exploration, second freestyle job running Python).

Job configs in this folder (posted to Jenkins via its `createItem` REST API instead of clicking
through the UI — same end result, scriptable and reproducible):

- [`my_first_job.xml`](my_first_job.xml) — echoes `hello world` plus `BUILD_ID`
  and `BUILD_URL`, restricted to the `docker-agent-alpine` label (see Lab 04).
- [`my_python_job.xml`](my_python_job.xml) — clones the fixture repo
  (`file:///repo`) and runs `python3 helloworld.py`, restricted to `docker-agent-python`, polls
  SCM every 5 minutes (`*/5 * * * *`).

## Steps actually run

```bash
cd labs
source 02_install_jenkins/scripts/_session.sh   # logs in, grabs a CSRF crumb, sets $JENKINS_URL/$AUTH
curl -b "$COOKIE_JAR" -u "$AUTH" -H "$CRUMB_HEADER" -H "Content-Type: application/xml" \
  --data-binary @03_freestyle_projects/my_first_job.xml "$JENKINS_URL/createItem?name=my_first_job"
curl -b "$COOKIE_JAR" -u "$AUTH" -H "$CRUMB_HEADER" -H "Content-Type: application/xml" \
  --data-binary @03_freestyle_projects/my_python_job.xml "$JENKINS_URL/createItem?name=my_python_job"
curl -b "$COOKIE_JAR" -u "$AUTH" -H "$CRUMB_HEADER" -X POST "$JENKINS_URL/job/my_first_job/build"
curl -b "$COOKIE_JAR" -u "$AUTH" -H "$CRUMB_HEADER" -X POST "$JENKINS_URL/job/my_python_job/build"
```

## Verification actually performed

`my_first_job` console output:

```
hello world
the build id of this job is 1
the build url is http://localhost:8081/job/my_first_job/1/
Finished: SUCCESS
```

`my_python_job` console output:

```
Cloning repository file:///repo
...
Checking out Revision 07c0efa... (refs/remotes/origin/master)
[my_python_job] $ /bin/sh -xe ...
+ python3 helloworld.py
Hello world
Finished: SUCCESS
```

## Bug hit and fixed along the way

`my_python_job` first failed with `can't open file '.../hello_world.py'` — the job config still
referenced the old filename from an earlier fixture draft, while the actual repo (synced from the
instructor's real `jenkins-101-master` folder) uses `helloworld.py`. Fixed by re-POSTing the
updated `config.xml` to the already-created job (`POST /job/my_python_job/config.xml`) before
rebuilding — this is the scripted equivalent of the video's "go into configure and fix it" step.
