# Step 07 — Write the deploy pipeline

**Goal:** author `.github/workflows/deploy.yml` that, on every push to `main`,
builds both service images, pushes them to ECR, and rolls each ECS service to the
new image — authenticating with **OIDC** (no stored AWS keys).

This is the core exercise. Build the file section by section below. By the end you
have one workflow that deploys **both** services from a single matrix job.

---

## A. Create the file

At the **root of your repo**, create the folders and file:

```
.github/workflows/deploy.yml
```

Build it up in the order of the sections below.

---

## B. Trigger, permissions, and env

```yaml
name: Deploy microservices to ECS

on:
  push:
    branches: [main]

permissions:
  id-token: write      # REQUIRED — lets the job request a GitHub OIDC token
  contents: read       # read the repo

env:
  AWS_REGION: eu-west-1          # must match the region you used in Step 05
  ECS_CLUSTER: microsvc-cluster  # must match your cluster name from Step 05
```

- `permissions.id-token: write` is what makes OIDC work. Without it,
  `configure-aws-credentials` has no token to exchange and the deploy fails before
  it starts.
- `AWS_REGION` and `ECS_CLUSTER` are referenced later as `${{ env.* }}`. Change
  them here if your region/cluster differ.

---

## C. The matrix — two services, one job

Both services build and deploy identically; only a handful of values differ. A
`strategy.matrix` runs the same steps once per service, in parallel.

```yaml
jobs:
  deploy:
    name: Deploy ${{ matrix.service.name }}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false           # one service failing must NOT cancel the other
      matrix:
        service:
          - name: inventory
            ecr_repo: inventory-service
            ecs_service: inventory-service
            task_def: inventory-service/task-definition.json
            container: inventory
          - name: orders
            ecr_repo: orders-service
            ecs_service: orders-service
            task_def: orders-service/task-definition.json
            container: orders
```

Each matrix entry carries everything that differs between the two services:

| key | what it is | where it must match |
|---|---|---|
| `name` | the service folder prefix (`inventory` → `inventory-service/`) | the folder you `docker build` |
| `ecr_repo` | the ECR repository name | the repos from Step 05 C |
| `ecs_service` | the ECS service name | the services from Step 06 |
| `task_def` | path to the task-definition JSON | the files you edited in Step 05 A |
| `container` | the container `name` inside that task def | the `name` field in the JSON |

`fail-fast: false` keeps the two deploys independent — if `inventory` fails,
`orders` still runs to completion (and vice versa).

---

## D. The steps

All steps live under the `deploy` job. Add them in order.

### D.1 — Checkout

```yaml
    steps:
      - name: Checkout
        uses: actions/checkout@v4
```

Needed so the runner has your `Dockerfile`s and `task-definition.json` files.

### D.2 — Authenticate to AWS with OIDC

```yaml
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}
```

- `role-to-assume` reads the repo **variable** you set in Step 04 B.3. Note it's
  `vars.` (variable), **not** `secrets.` — a secret resolves empty here.
- No `aws-access-key-id` / `aws-secret-access-key` anywhere. With
  `id-token: write` set (Section B), this action exchanges the OIDC token for
  temporary credentials.

### D.3 — Log in to ECR

```yaml
      - name: Log in to Amazon ECR
        id: ecr
        uses: aws-actions/amazon-ecr-login@v2
```

`id: ecr` lets later steps read its `registry` output
(`${{ steps.ecr.outputs.registry }}` = `<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com`).

### D.4 — Build and push the image

```yaml
      - name: Build and push image
        env:
          REGISTRY: ${{ steps.ecr.outputs.registry }}
        run: |
          IMAGE="$REGISTRY/${{ matrix.service.ecr_repo }}:${{ github.sha }}"
          docker build -t "$IMAGE" ./${{ matrix.service.name }}-service
          docker push "$IMAGE"
          echo "IMAGE=$IMAGE" >> "$GITHUB_ENV"
```

- Tags the image with `${{ github.sha }}` (the commit SHA), **not** `latest` — so
  every deploy is a distinct, traceable image and ECS sees a real change to roll
  to.
- Builds from `./<name>-service` (e.g. `./inventory-service`), the folder holding
  that service's `Dockerfile`.
- `echo "IMAGE=..." >> "$GITHUB_ENV"` exports the full image URI so the next step
  can read it as `${{ env.IMAGE }}`.

### D.5 — Render the task definition with the new image

```yaml
      - name: Render task definition
        id: render
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: ${{ matrix.service.task_def }}
          container-name: ${{ matrix.service.container }}
          image: ${{ env.IMAGE }}
```

Takes the committed `task-definition.json`, swaps the `image` of the container
named `container-name`, and writes a new rendered file. `container-name` **must**
equal the `name` inside the JSON (`inventory` / `orders`) or it patches nothing.

### D.6 — Deploy to ECS

```yaml
      - name: Deploy to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: ${{ steps.render.outputs.task-definition }}
          service: ${{ matrix.service.ecs_service }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true
```

- Feeds the **rendered** file (`steps.render.outputs.task-definition`) — the one
  with the new image — into the deploy.
- Registers a new task-definition revision and updates the matching ECS service.
- `wait-for-service-stability: true` makes the job wait until ECS finishes the
  rollout, so a failed rollout fails the job instead of going green prematurely.

---

## E. Verify the file before pushing

- [ ] `env.AWS_REGION` and `env.ECS_CLUSTER` match Step 05 (e.g. `eu-west-1`, `microsvc-cluster`)
- [ ] `role-to-assume` uses `vars.AWS_DEPLOY_ROLE_ARN` (variable, not secret)
- [ ] **No** `aws-access-key-id` / `aws-secret-access-key` anywhere
- [ ] Each matrix `container` matches the `name` field in that service's `task-definition.json`
- [ ] Each matrix `task_def` path points at the real file
- [ ] Build context `./<name>-service` matches the folder with the `Dockerfile`
- [ ] Every action is pinned to a major version tag (`@v4`, `@v2`, `@v1`) — not `@main` or a full SHA

Don't push yet — that's [Step 08](08-deploy-and-verify.md), where this first run
finally brings the services up from running count 0.

---

## Self-check

- What breaks if you forget `permissions: id-token: write`?
- Why `fail-fast: false` — what would the default do to `orders` if `inventory` fails?
- Why tag images with `github.sha` instead of `latest`?
- Why does the deploy step use `steps.render.outputs.task-definition` and not the original `task_def` path?

## What you learned

- A single matrix job deploys N independent services, each with its own registry,
  task definition, and ECS service. OIDC + the AWS actions turn
  "build → push → render → deploy" into a declarative, keyless pipeline.

## Next

→ [Step 08 — Deploy & verify end-to-end](08-deploy-and-verify.md)
