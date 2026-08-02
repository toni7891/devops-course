# Step 08 – Set Up AWS OIDC for GitHub Actions

## Goal

Allow GitHub Actions to authenticate to AWS securely using OpenID Connect (OIDC), without storing long-lived AWS Access Keys as secrets.

---

## Why OIDC Instead of Access Keys?

Static AWS Access Keys are a security risk:
- They don't expire automatically
- If leaked (e.g. accidentally committed to Git), they can be used by anyone
- They require manual rotation

**OIDC** solves this by using short-lived, automatically rotated tokens:
- GitHub generates a token for each workflow run
- AWS validates the token against the GitHub OIDC provider
- AWS issues a temporary credential with a limited lifetime
- No secrets are stored anywhere

---

## How It Works (Conceptual)

1. GitHub Actions sends a request to AWS with a signed JWT token
2. AWS checks the token against the trusted **OIDC Identity Provider** you register
3. If valid, AWS allows the workflow to **assume an IAM Role**
4. The role has a **permission policy** that grants access to S3 and CloudFront
5. The credentials are valid only for the duration of the workflow run

---

## Tasks

### 1. Register GitHub as an OIDC Identity Provider in AWS

In the AWS Console (or via Terraform), create an **IAM Identity Provider** for GitHub Actions.

You will need:
- **Provider URL:** the GitHub OIDC URL (look this up in GitHub's documentation)
- **Audience:** the value that GitHub sets as the audience in the JWT token

> This step tells AWS: "I trust tokens issued by GitHub"

---

### 2. Create an IAM Role for GitHub Actions

Create an IAM Role that GitHub Actions workflows can assume.

The role needs:

**Trust Policy (who can assume this role):**
- The principal must be the OIDC identity provider you just created
- The condition must restrict which GitHub repository (and optionally which branch) can assume the role

> Be specific in your condition. A condition that allows any GitHub repo to assume the role is a security risk.

**Permission Policy (what the role can do):**

The role needs permission to:
- Upload files to S3 (`s3:PutObject`, `s3:DeleteObject`, `s3:ListBucket`)
- Create a CloudFront cache invalidation (`cloudfront:CreateInvalidation`)

> Use the **principle of least privilege** — grant only what is needed, nothing more.

---

### 3. Save the Role ARN

After creating the role, copy its ARN.

You will need this in the next step when configuring the GitHub Actions workflow.

---

### 4. Store Required Values as GitHub Secrets

In your GitHub repository settings, add the following secrets:

| Secret Name | Value |
|-------------|-------|
| `AWS_ROLE_ARN` | The ARN of the IAM role you just created |
| `AWS_REGION` | Your AWS region (e.g. `us-east-1`) |
| `S3_BUCKET_NAME` | The name of your S3 bucket |
| `CLOUDFRONT_DISTRIBUTION_ID` | The ID of your CloudFront distribution |

> You retrieved the last two values from Terraform outputs in the previous step.

---

## Key Concepts

- **OIDC Provider** — a trusted issuer of identity tokens registered in AWS IAM
- **Trust Policy** — the part of an IAM Role that controls *who* can assume it
- **Permission Policy** — the part of an IAM Role that controls *what* it can do
- The `sts:AssumeRoleWithWebIdentity` action is what makes OIDC role assumption possible
- GitHub's OIDC token contains claims like `repo`, `ref`, and `environment` that you can use in conditions

---

## Check

Before moving on, confirm:

- [ ] GitHub OIDC Identity Provider is registered in AWS IAM
- [ ] IAM Role exists with the correct trust and permission policies
- [ ] Trust policy is scoped to your specific GitHub repository
- [ ] GitHub Secrets are set for role ARN, region, bucket name, and distribution ID

---

**Previous:** [Step 07 – Apply Your Infrastructure](07-terraform-apply.md)  
**Next:** [Step 09 – Write the GitHub Actions Workflow](09-github-actions-workflow.md)
