# Step 09 – Write the GitHub Actions Workflow

## Goal

Create a GitHub Actions workflow that runs Terraform only when infrastructure files change, and deploys the app only when application code changes — with the constraint that deploy never runs if Terraform failed.

---

## Where Workflows Live

GitHub Actions workflows are YAML files stored in:

```
.github/
└── workflows/
    └── deploy.yml
```

---

## Workflow Architecture

The workflow has **three jobs**:

```
Job 1: changes  (always runs)
  └── Detects which paths changed
         ↓                  ↓
  terraform == true    app == true

Job 2: terraform         Job 3: deploy
  (only if terraform       (only if app changed
   files changed)           AND terraform didn't fail)
```

This ensures:
- Pushing only app code → only the `deploy` job runs (Terraform is skipped)
- Pushing only Terraform code → only the `terraform` job runs (deploy is skipped)
- Pushing both → `terraform` runs first, then `deploy` runs if it succeeded
- If `terraform` fails → `deploy` is blocked

---

## Tasks

### 1. Define the Trigger

Trigger on push to `main` and also add `workflow_dispatch` so it can be run manually.

```yaml
on:
  push:
    branches:
      - main
  workflow_dispatch:
```

> `workflow_dispatch` allows triggering the workflow from the GitHub UI without a code push. When triggered manually, both jobs should run regardless of what files changed.

---

### 2. Set Workflow-Level Permissions

OIDC requires the workflow to be able to request an identity token:

```yaml
permissions:
  id-token: write
  contents: read
```

---

### 3. Job 1 – Detect Changes

This job runs on every push and produces two boolean outputs: `terraform` and `app`.

Use the **`dorny/paths-filter@v3`** action to check which paths changed in the commit.

```yaml
jobs:
  changes:
    name: Detect Changes
    runs-on: ubuntu-latest
    outputs:
      terraform: ...
      app: ...
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            terraform:
              - 'terraform/**'
            app:
              - 'app/**'
```

**For the outputs**, combine the filter result with a check for manual dispatch:

```
terraform: ${{ steps.filter.outputs.terraform == 'true' || github.event_name == 'workflow_dispatch' }}
app:       ${{ steps.filter.outputs.app == 'true'       || github.event_name == 'workflow_dispatch' }}
```

> Without the `|| github.event_name == 'workflow_dispatch'` part, manual triggers would skip both jobs because no files "changed".

---

### 4. Job 2 – Terraform

This job should:
- Declare `needs: changes`
- Have an `if:` condition that checks `needs.changes.outputs.terraform == 'true'`
- Use `defaults.run.working-directory: terraform` so every step runs in the right folder

Steps:

| Step | Action/Command |
|------|---------------|
| Checkout | `actions/checkout@v4` |
| Setup Terraform | `hashicorp/setup-terraform@v3` |
| AWS credentials (OIDC) | `aws-actions/configure-aws-credentials@v4` |
| `terraform init` | Connects to the S3 backend and downloads state |
| `terraform fmt -check` | Fails if code is not formatted — enforces style in CI |
| `terraform validate` | Checks for syntax and reference errors |
| `terraform plan -out=tfplan` | Saves the plan to a file |
| `terraform apply -auto-approve tfplan` | Applies exactly the saved plan |

> Saving the plan with `-out` and then applying from the file ensures apply only does what plan reviewed. Never skip the `-out` / file pattern in CI.

---

### 5. Job 3 – Deploy

This job must:
- Declare `needs: [changes, terraform]`
- Have an `if:` condition using `always()` to prevent automatic skipping when the `terraform` job was skipped

The `if:` condition must express three things at once:

```yaml
if: |
  always() &&
  needs.changes.outputs.app == 'true' &&
  (needs.terraform.result == 'success' || needs.terraform.result == 'skipped')
```

**Why `always()`?**

By default, GitHub Actions skips a job if any of its `needs` were skipped. Without `always()`, when `terraform` is skipped (because only app code changed), `deploy` would also be automatically skipped — even though we want it to run.

**Why check `terraform.result`?**

If `terraform` ran and **failed**, `deploy` must not proceed. If it was skipped (infrastructure unchanged) or succeeded, `deploy` is safe to continue.

Steps:

| Step | Action/Command |
|------|---------------|
| Checkout | `actions/checkout@v4` |
| Setup Node.js | `actions/setup-node@v4` with `cache: 'npm'` |
| Install deps | `npm ci` (in `app/` directory) |
| Build | `npm run build` (in `app/` directory) |
| AWS credentials (OIDC) | Re-configure — OIDC credentials don't carry between jobs |
| Upload to S3 | `aws s3 sync app/dist/ s3://<bucket>/ --delete` |
| Invalidate cache | `aws cloudfront create-invalidation ...` |

---

### 6. GitHub Secrets to Configure

Set these in your repo under `Settings → Secrets and variables → Actions`:

| Secret | Where to get the value |
|--------|----------------------|
| `AWS_ROLE_ARN` | Terraform output: `github_deploy_role_arn` |
| `AWS_REGION` | The region you deployed to |
| `S3_BUCKET_NAME` | Terraform output: `s3_bucket_name` |
| `CLOUDFRONT_DISTRIBUTION_ID` | Terraform output: `cloudfront_distribution_id` |

---

## Behaviour Summary

| What changed | terraform job | deploy job |
|-------------|--------------|-----------|
| `terraform/` only | runs | skipped |
| `app/` only | skipped | runs |
| both | runs | runs (after terraform) |
| terraform fails | fails | blocked |
| `workflow_dispatch` | runs | runs |

---

## Check

Before moving on, confirm:

- [ ] `changes` job outputs are set for both `terraform` and `app`
- [ ] `workflow_dispatch` override is included in the outputs
- [ ] `terraform` job has `if: needs.changes.outputs.terraform == 'true'`
- [ ] `deploy` job has `needs: [changes, terraform]` and the `always()` condition
- [ ] `deploy` checks that terraform either succeeded or was skipped
- [ ] All 4 GitHub Secrets are set in the repository
- [ ] Test: push only an app change → only deploy runs
- [ ] Test: push only a Terraform change → only terraform runs

---

**Previous:** [Step 08 – AWS OIDC Setup](08-aws-oidc-setup.md)  
**Next:** [Step 10 – Validate the Full Deployment](10-validation.md)
