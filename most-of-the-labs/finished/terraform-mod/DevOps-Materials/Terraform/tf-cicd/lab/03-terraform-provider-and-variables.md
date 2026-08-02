# Step 03 – Configure the Terraform Provider and Variables

## Goal

Configure the AWS provider and declare the input variables your infrastructure will use.

---

## Part A – Terraform Provider

The **provider block** tells Terraform which cloud platform to use and how to authenticate.

### Tasks

#### 1. Declare the Required Provider

In your `provider.tf`, specify that you need the `hashicorp/aws` provider.  
You should pin it to a specific version range to ensure reproducible builds.

> Think about: what happens if you don't pin the version and a breaking change is released?

---

#### 2. Configure the AWS Provider

The provider needs to know which AWS region to deploy resources into.

Rather than hardcoding the region, reference a variable so it can be changed easily later.

> Consider: should you set a sensible default, or require it to always be provided explicitly?

---

#### 3. Run `terraform init`

Once your provider is configured, initialize the Terraform working directory.

This downloads the provider plugin and sets up the backend.

> What does the `.terraform.lock.hcl` file do? Should you commit it?

---

## Part B – Variables

Variables make your Terraform code reusable and configurable.

### Tasks

#### 4. Declare Your Variables

In `variables.tf`, declare variables for the values you identified in the previous step.

For each variable, think about:
- What **type** is it? (`string`, `number`, `bool`, `list`, `map`)
- Should it have a **default** value, or be required?
- Add a meaningful **description** so others understand its purpose

---

#### 5. Set Variable Values

In `terraform.tfvars`, provide concrete values for your variables.

> Example values to set: your AWS region, a unique bucket name, a project prefix.  
> Bucket names must be globally unique across all of AWS — factor that into your naming.

---

#### 6. Use Locals (Optional but Recommended)

Consider using a `locals` block to derive computed values from your variables.

For example: combining a project prefix with an environment name to build consistent resource names.

> Locals are great for keeping naming conventions consistent without repeating yourself.

---

## Key Concepts

- The `terraform` block with `required_providers` pins your provider versions.
- The `provider` block configures the provider's behavior (region, credentials, etc.).
- Variables declared in `variables.tf` + values from `terraform.tfvars` = your configuration inputs.
- Never hardcode AWS credentials in Terraform files.

---

## Check

Before moving on, confirm:

- [ ] `terraform init` completes without errors
- [ ] Your variables are declared with types and descriptions
- [ ] `terraform.tfvars` has real values for your variables
- [ ] The provider is configured to use a variable for the region

---

**Previous:** [Step 02 – Terraform Project Structure](02-terraform-project-structure.md)  
**Next:** [Step 04 – Provision the S3 Bucket](04-terraform-s3-bucket.md)
