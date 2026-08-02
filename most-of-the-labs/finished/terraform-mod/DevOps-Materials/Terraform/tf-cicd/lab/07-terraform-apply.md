# Step 07 – Apply Your Infrastructure

## Goal

Validate and apply your Terraform configuration to provision the actual AWS resources.

---

## Before You Apply

Make sure you have:

- AWS credentials configured locally (via `aws configure`, environment variables, or an AWS profile)
- The correct AWS region set
- `terraform init` completed successfully
- All `.tf` files saved

---

## Tasks

### 1. Format Your Code

Run the Terraform formatter to ensure consistent code style.

```
terraform fmt
```

This modifies files in place. If any files were changed, review the diff.

> Consider adding `terraform fmt -check` as a pre-apply habit or CI step.

---

### 2. Validate Your Configuration

Run the Terraform validator to catch syntax errors and invalid references before applying.

```
terraform validate
```

Fix any errors before proceeding.

> Validate does not check that your resource values are correct (e.g. a wrong bucket name). It only checks that the configuration is structurally valid.

---

### 3. Review the Plan

Run `terraform plan` and read the output carefully.

- How many resources will be created?
- Are there any unexpected changes or deletions?
- Do the resource names and values match what you expect?

> Never skip the plan step. A plan shows exactly what Terraform intends to do before touching any real infrastructure.

---

### 4. Apply the Configuration

Once you are confident the plan looks correct, apply it.

```
terraform apply
```

Type `yes` when prompted to confirm.

> CloudFront distributions take **5–15 minutes** to fully deploy. The `terraform apply` command may take a while — this is normal. Do not interrupt it.

---

### 5. Review the Outputs

After apply completes, Terraform will print your outputs.

- Copy the **CloudFront domain name** — you will need it to verify the deployment.
- Copy the **S3 bucket name** — you will need it for the CI/CD pipeline.
- Copy the **CloudFront distribution ID** — you will need it for cache invalidation.

---

### 6. Verify in the AWS Console

Log into the AWS Console and confirm:

- The S3 bucket exists
- Public access is blocked on the bucket
- The CloudFront distribution is in **Deployed** status
- The distribution's origin points to your S3 bucket

---

## If Something Goes Wrong

- Run `terraform plan` again to see the current state vs desired state.
- Check the error message carefully — Terraform errors are usually descriptive.
- Use `terraform destroy` to tear everything down if you need a clean start.
- Check that your IAM user/role has permissions to create the required resources.

---

## Key Concepts

- `terraform fmt` → formats code
- `terraform validate` → checks for syntax/reference errors
- `terraform plan` → shows what will change (no real changes made)
- `terraform apply` → makes the actual changes
- `terraform destroy` → removes all managed resources

---

## Check

Before moving on, confirm:

- [ ] `terraform validate` passes with no errors
- [ ] `terraform apply` completes successfully
- [ ] You can see all outputs in the terminal
- [ ] The CloudFront distribution is **Deployed** in the AWS Console
- [ ] You have saved the CloudFront URL, bucket name, and distribution ID

---

**Previous:** [Step 06 – Define Terraform Outputs](06-terraform-outputs.md)  
**Next:** [Step 08 – Set Up AWS OIDC for GitHub Actions](08-aws-oidc-setup.md)
