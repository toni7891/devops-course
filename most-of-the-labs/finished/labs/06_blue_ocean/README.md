# Lab 06 — Blue Ocean

Corresponds to transcript chunks `29` and `30` (Blue Ocean interface, course wrap-up).

Blue Ocean ships as a plugin baked into the master image (`docker/plugins.txt`), so there's no
separate install step — it's reachable as soon as Jenkins is up.

## Verification actually performed

```
$ curl -s -o /dev/null -w "%{http_code}" -u admin:admin http://localhost:8081/blue/organizations/jenkins/pipelines/
200

$ curl -u admin:admin http://localhost:8081/blue/rest/organizations/jenkins/pipelines/my_first_build_pipeline/runs/4/nodes/
Build     SUCCESS
Test      SUCCESS
Deliver   SUCCESS
```

The Blue Ocean REST API returns the same three pipeline stages from Lab 05's run, each reported
`SUCCESS` — matching what the classic Jenkins stage-view already showed, just through Blue Ocean's
nicer API/UI. To browse it visually: open `http://localhost:8081/blue` and sign in with
`admin`/`admin`.
