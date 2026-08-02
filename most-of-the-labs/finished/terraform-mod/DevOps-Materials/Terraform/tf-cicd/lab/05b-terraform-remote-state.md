# Step 05b – Configure Remote State Backend (S3)

## Goal

Store Terraform state in an S3 bucket so that CI/CD pipelines (and multiple team members) can share and safely modify infrastructure state.

---

## Why This Step Comes Before CI/CD

By default, Terraform stores state in a local `terraform.tfstate` file. This is fine for local development, but breaks in CI/CD because:

- Each workflow run starts on a **fresh runner** with no local files
- Two concurrent runs could corrupt the state
- There is no audit trail of state changes

The solution is a **remote backend** — Terraform reads and writes state to an S3 bucket, and uses native S3 locking to prevent concurrent runs.

---

## The Bootstrapping Problem

The state bucket must exist **before** Terraform can use it as a backend.  
You can't manage the state bucket with the same Terraform that uses it for state.

**Solution:** Create the state bucket once via the AWS CLI (or the console), then configure Terraform to use it. This is a one-time manual step.

---

## Tasks

### 1. Create the State Bucket

Use the AWS CLI to create a dedicated S3 bucket for Terraform state.

Choose a globally unique name. A reliable pattern: `<project>-tfstate-<account-id>`

After creating the bucket:
- Enable **versioning** — this lets you recover previous state versions
- Enable **public access block** — state files contain sensitive resource details

> This bucket should NOT be managed by the Terraform you're about to run. Create it separately.

---

### 2. Configure the S3 Backend in Terraform

Add a `backend "s3"` block inside your `terraform` block in `provider.tf`.

Required arguments:
- `bucket` — the name of the state bucket you just created
- `key` — the path within the bucket where state will be stored (e.g. `prod/terraform.tfstate`)
- `region` — the AWS region of the state bucket
- `use_lockfile` — set to `true` to enable native S3 state locking (requires Terraform >= 1.10)
- `encrypt` — set to `true` to encrypt the state file at rest

> The backend block does **not** support variable references — values must be literal strings.

---

### 3. Re-initialize Terraform

After adding the backend block, run `terraform init` again.

Terraform will detect the new backend and ask if you want to migrate your existing local state to S3.

Answer **yes**.

---

### 4. Verify State Is in S3

After init, check the S3 bucket in the AWS Console or via CLI:

```
aws s3 ls s3://<your-state-bucket>/<key-prefix>/
```

You should see the `terraform.tfstate` file.

---

### 5. Update the IAM Role with State Permissions

The GitHub Actions role needs permission to read and write the state bucket.

Add these permissions to your IAM role policy:

| Action | Resource |
|--------|---------|
| `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`, `s3:ListBucket` | the state bucket and its objects |

> Without these, `terraform init` in CI/CD will fail with an access denied error.

---

## Key Concepts

- Remote state is shared — everyone and every pipeline sees the same infrastructure state
- `use_lockfile = true` prevents two Terraform runs from updating state simultaneously using S3's conditional write feature
- The `key` in the backend config is the S3 object path — different environments should use different keys (e.g. `dev/terraform.tfstate`, `prod/terraform.tfstate`)
- Never commit `terraform.tfstate` to Git — add it to `.gitignore`

---

## .gitignore for Terraform

Make sure your `.gitignore` includes:

```
.terraform/
*.tfstate
*.tfstate.backup
tfplan
*.tfplan
```

---

## Check

Before moving on, confirm:

- [ ] State bucket exists and has versioning + public access block enabled
- [ ] `provider.tf` has the `backend "s3"` block with correct values
- [ ] `terraform init` migrated local state to S3 without errors
- [ ] State file is visible in the S3 bucket
- [ ] IAM role has `s3:GetObject` / `s3:PutObject` on the state bucket

---

**Previous:** [Step 05 – CloudFront](05-terraform-cloudfront.md)  
**Next:** [Step 06 – Terraform Outputs](06-terraform-outputs.md)
