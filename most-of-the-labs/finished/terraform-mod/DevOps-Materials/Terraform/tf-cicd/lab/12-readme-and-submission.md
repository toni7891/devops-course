# Step 12 – Write the README and Prepare Submission

## Goal

Write a professional README for your repository and prepare all required submission materials.

---

## README Requirements

Your `README.md` must include the following sections:

---

### 1. Project Overview

Write 2–4 sentences explaining what this project does at a high level.

> Who is this for? What problem does it solve? What technologies are involved?

---

### 2. Architecture Diagram

Embed your architecture diagram image directly in the README.

> Use a relative path to reference the image file in your repository.

---

### 3. AWS Component Descriptions

Write a short paragraph or bullet list explaining the role of each AWS service used:

- **Amazon S3** — why is it used here? what does it store?
- **Amazon CloudFront** — what does it add? why not serve from S3 directly?
- **IAM Role (OIDC)** — what problem does it solve compared to Access Keys?

---

### 4. Deployment Instructions

Write step-by-step instructions that would allow another developer to deploy this project from scratch.

Include:
- Prerequisites (what tools and accounts are needed)
- How to set up the Terraform infrastructure
- How to configure the GitHub repository (secrets, OIDC)
- How to trigger a deployment

> Write this as if your reader is a competent developer who has never seen this project before.

---

### 5. Website URL

Include the live CloudFront URL where the deployed application is accessible.

---

## Repository Structure

Before submitting, confirm your repository contains:

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml
├── terraform/           (or infra/ or whatever you named it)
│   ├── main.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
├── react-app/           (the provided React application)
├── architecture.drawio
├── architecture.png     (screenshot of the diagram)
└── README.md
```

> Adjust paths to match your actual structure.

---

## Submission Checklist

| Item | Required |
|------|----------|
| GitHub repository URL | Yes |
| Terraform source code | Yes |
| GitHub Actions workflow file | Yes |
| Screenshot of successful pipeline run | Yes |
| Working CloudFront URL | Yes |
| `architecture.drawio` file | Yes |
| Screenshot of the architecture diagram | Yes |
| `README.md` with all required sections | Yes |

---

## Before You Submit

- [ ] `terraform validate` passes on your Terraform code
- [ ] `terraform fmt` has been run — all files are properly formatted
- [ ] The GitHub Actions workflow runs successfully on push to `main`
- [ ] The CloudFront URL loads the application
- [ ] The README is complete and professionally written
- [ ] The architecture diagram includes all required components and both flows
- [ ] All files listed above are committed and pushed to your GitHub repository

---

**Previous:** [Step 11 – Architecture Diagram](11-architecture-diagram.md)  
**Next:** [Step 13 – Bonus Challenges (Optional)](13-bonus-challenges.md)
