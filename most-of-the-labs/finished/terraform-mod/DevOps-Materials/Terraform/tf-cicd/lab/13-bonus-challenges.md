# Step 13 – Bonus Challenges (Optional)

## Goal

Extend your solution with production-quality improvements to earn additional points and deepen your understanding.

Each challenge below is independent — you can complete any combination of them.

---

## Bonus 1 – Terraform Modules

Refactor your Terraform code into reusable **modules**.

For example, split your infrastructure into:
- A `s3` module
- A `cloudfront` module

Each module should have its own `variables.tf`, `main.tf`, and `outputs.tf`.

> Think about: what inputs does each module need? What should it expose as outputs?

**Why this matters:** Modules make Terraform code reusable across projects and environments.

---

## Bonus 2 – Locals

Add a `locals` block to derive computed values used across your configuration.

Good candidates for locals:
- Constructed resource names (e.g. `"${var.project}-${var.environment}-bucket"`)
- Common tags merged into a map
- Repeated string values used in multiple places

> Locals reduce repetition and make your code easier to refactor.

---

## Bonus 3 – tfvars for Multiple Environments

Organize your variable values to support multiple environments (e.g. `dev` and `prod`).

Create separate `tfvars` files:
- `dev.tfvars`
- `prod.tfvars`

Each file provides environment-specific values (different bucket names, different regions, etc.).

Use `terraform apply -var-file=dev.tfvars` to select the environment.

> Think about: how would your resource naming convention change between environments?

---

## Bonus 4 – npm Dependency Caching in GitHub Actions

Add caching to the **Install Dependencies** step in your workflow.

GitHub Actions has a built-in `cache` action, and the `setup-node` action also supports caching natively.

When caching works:
- A cache hit skips the `npm install` entirely
- Workflow run time drops significantly on repeated runs

> Verify that caching is working by checking the step log — it should say "Cache restored" on a hit.

---

## Bonus 5 – Workflow Artifacts

Upload the React build output as a **workflow artifact** so it can be downloaded from the Actions UI.

This is useful for:
- Debugging build output without re-running the workflow
- Auditing exactly what was deployed

> Artifacts are stored for a configurable number of days (90 by default).

---

## Bonus 6 – Terraform Format & Validate Job

Add a separate **job** to your GitHub Actions workflow that runs `terraform fmt -check` and `terraform validate` before the deploy job.

The deploy job should only run if this check job passes.

> Use `needs:` in GitHub Actions to create job dependencies.

---

## Bonus 7 – Deploy Only When Application Changes

Modify your workflow so the deployment step only runs when files in the React application directory have changed.

> GitHub Actions has a `paths` filter on the trigger — and there are also third-party actions for change detection.

This prevents unnecessary deployments when only Terraform or documentation files change.

---

## Bonus 8 – Consistent Naming Convention

Apply a consistent naming convention to all AWS resources.

A common pattern: `{project}-{environment}-{resource-type}`

For example:
- `myapp-prod-bucket`
- `myapp-prod-cloudfront`

Use locals or variables to enforce this consistently without repeating yourself.

---

## Bonus 9 – AWS Resource Tagging

Apply a standard set of tags to **all** AWS resources.

Recommended tags:
- `Project`
- `Environment`
- `ManagedBy` (set to `"terraform"`)
- `Owner`

Use a `locals` map for the common tags and merge it into each resource's `tags` argument.

> Tagging is a fundamental best practice for cost management and resource ownership in real AWS environments.

---

## How Bonuses Are Evaluated

Bonuses are assessed on:
- **Correctness** — does it actually work as intended?
- **Integration** — is it woven into the existing solution cleanly?
- **Understanding** — can you explain why you made the choices you did?

---

**Previous:** [Step 12 – README and Submission](12-readme-and-submission.md)  
**Back to Start:** [Step 00 – Overview](00-overview.md)
