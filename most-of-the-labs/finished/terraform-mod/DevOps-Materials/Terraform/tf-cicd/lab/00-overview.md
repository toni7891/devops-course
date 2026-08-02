# Lab Overview

## Scenario

Your company, **Cloud Academy**, has completed the development of a React-based marketing website. The application is ready for production, but no cloud infrastructure or deployment process currently exists.

As a DevOps Engineer, your responsibility is to provision the required AWS infrastructure using **Terraform** and build a complete **CI/CD pipeline** using **GitHub Actions**.

The application source code is already provided. Your task is to automate its deployment.

---

## Objective

By the end of this lab, you will have:

- Infrastructure provisioned with Terraform
- A React application hosted on Amazon S3
- Global content delivery through CloudFront
- A fully automated CI/CD pipeline using GitHub Actions
- Secure authentication to AWS using OIDC (without static Access Keys)
- Complete project documentation
- A Draw.io architecture diagram

---

## Prerequisites

Before starting, make sure you are comfortable with:

- Git & GitHub (branching, pushing, repos)
- GitHub Actions (workflows, jobs, steps, secrets)
- AWS IAM (roles, policies, trust relationships)
- OIDC (how federated identity works with AWS)
- Amazon S3 (buckets, policies, static hosting concepts)
- Amazon CloudFront (distributions, origins, cache invalidation)
- Terraform (providers, resources, variables, outputs)
- Basic React (you will not write any application code)

---

## Lab Structure

| Step | Topic |
|------|-------|
| 01 | Explore the provided React application |
| 02 | Set up your Terraform project structure |
| 03 | Configure the Terraform provider and variables |
| 04 | Provision the S3 bucket |
| 05 | Provision CloudFront with Origin Access Control |
| 05b | Configure remote state backend (S3) |
| 06 | Define Terraform outputs |
| 07 | Apply your infrastructure |
| 08 | Set up AWS OIDC for GitHub Actions |
| 09 | Write the GitHub Actions workflow (changes detection + Terraform + Deploy jobs) |
| 10 | Validate the full deployment |
| 11 | Create the architecture diagram |
| 12 | Write the README and prepare submission |
| 13 | Bonus challenges |

---

## Target Architecture

```
          Developer
              |
              | git push
              ▼
     GitHub Repository
              |
              ▼
     GitHub Actions
     ┌──────────────────┐
     │ Build React      │
     │ OIDC Auth        │
     │ Upload to S3     │
     │ Invalidate Cache │
     └────────┬─────────┘
              |
              ▼
     IAM Role (OIDC)
              |
              ▼
     Amazon S3 Bucket
              |
              ▼
     CloudFront Distribution
              |
              ▼
     Browser / End Users
```

---

**Next:** [Step 01 – Explore the React Application](01-explore-the-app.md)
