# Step 06 – Define Terraform Outputs

## Goal

Expose key values from your infrastructure so they are easy to retrieve after `terraform apply`.

---

## Why Outputs Matter

Outputs serve two purposes:

1. **Human convenience** — after running `terraform apply`, outputs are printed to the terminal so you can immediately see important values (like your CloudFront URL) without opening the AWS Console.
2. **Automation** — other tools or pipelines can query Terraform outputs programmatically using `terraform output`.

---

## Tasks

### 1. Identify What to Expose

Think about which values a person would need after provisioning this infrastructure.

Useful outputs for this project likely include:

- The **S3 bucket name** — needed by the CI/CD pipeline to upload files
- The **S3 bucket ARN** — useful for reference and debugging
- The **CloudFront distribution ID** — needed by the CI/CD pipeline to invalidate the cache
- The **CloudFront domain name** — the URL where the application will be accessible

---

### 2. Define the Outputs

In your `outputs.tf`, define one `output` block for each value.

For each output:
- Give it a clear, descriptive **name** (use underscores, not dashes)
- Write a **description** so it's self-documenting
- Set the **value** using a reference to the relevant Terraform resource attribute

> Avoid hardcoding values in outputs. Always reference the resource attributes.

---

### 3. Consider Sensitive Outputs

Some output values may contain sensitive information (like secrets or tokens).

> For this lab, none of your outputs should be sensitive — but it's good practice to know that Terraform has a `sensitive = true` option that hides the value from terminal output.

---

## Verifying Outputs

After running `terraform apply` later, you can:

- See all outputs printed at the end of the apply
- Run `terraform output` to see them again at any time
- Run `terraform output <output_name>` to retrieve a single value

---

## Key Concepts

- Outputs are defined with the `output` block in `outputs.tf`
- Output values reference resource attributes using the format: `resource_type.resource_name.attribute`
- Outputs do not create infrastructure — they just surface information

---

## Check

Before moving on, confirm:

- [ ] You have at least 4 outputs defined
- [ ] Each output has a `description`
- [ ] Values are referenced from resources (not hardcoded)
- [ ] You know which outputs the CI/CD pipeline will need later (bucket name and CloudFront ID)

---

**Previous:** [Step 05 – Provision CloudFront](05-terraform-cloudfront.md)  
**Next:** [Step 07 – Apply Your Infrastructure](07-terraform-apply.md)
