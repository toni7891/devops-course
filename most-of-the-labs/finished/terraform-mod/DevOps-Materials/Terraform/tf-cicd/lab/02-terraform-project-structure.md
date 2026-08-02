# Step 02 – Set Up Your Terraform Project Structure

## Goal

Create a clean, organized Terraform project that will hold all your infrastructure code.

---

## Why Structure Matters

A well-organized Terraform project is easier to read, maintain, and extend.  
Separating concerns into different files is a widely adopted convention.

---

## Recommended File Layout

Inside your repository, create a folder to hold your Terraform code (for example, `terraform/` or `infra/`).

Inside that folder, create the following empty files to start with:

| File | Purpose |
|------|---------|
| `main.tf` | Primary resource definitions |
| `provider.tf` | AWS provider configuration |
| `variables.tf` | Input variable declarations |
| `outputs.tf` | Output value definitions |
| `terraform.tfvars` | Actual variable values (do not commit secrets here) |

> You can split resources further (e.g. `s3.tf`, `cloudfront.tf`) if you prefer. This is a matter of style — what matters is consistency.

---

## Tasks

### 1. Create the Terraform Directory

Add a dedicated directory inside your repository for Terraform files.

> Consider: should this be at the root of the repo, or in a subdirectory?

---

### 2. Create the Starter Files

Create the files listed in the table above. They can be empty for now — you will fill them in the next steps.

---

### 3. Add a `.gitignore` for Terraform

Terraform generates files that should not be committed to version control.

Research which Terraform files and directories are typically excluded from Git.

> Hint: think about the `.terraform/` directory, lock files, and state files.

---

### 4. Plan Your Variables

Before writing any resources, think about what values might change between environments or deployments.

Good candidates for variables include:
- AWS region
- S3 bucket name
- Project name or prefix
- Environment name (dev, prod, etc.)

Write down a list. You'll declare these in `variables.tf` in the next step.

---

## Key Concepts

- **`variables.tf`** declares *what* variables exist and their types/defaults.
- **`terraform.tfvars`** provides *actual values* for those variables.
- **`outputs.tf`** exposes values from your infrastructure after `apply`.

---

**Previous:** [Step 01 – Explore the App](01-explore-the-app.md)  
**Next:** [Step 03 – Configure the Terraform Provider and Variables](03-terraform-provider-and-variables.md)
