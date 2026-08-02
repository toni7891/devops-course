# Step 11 – Create the Architecture Diagram

## Goal

Design a professional architecture diagram using **Draw.io (diagrams.net)** that visually represents the full deployment.

---

## Important Requirement

> **AI-generated diagrams are NOT allowed.**

You must create the diagram yourself in Draw.io. This exercises your ability to understand and communicate system design — not just implement it.

---

## Tool

Use **[diagrams.net](https://app.diagrams.net)** (also known as Draw.io).

You can:
- Use the web version at `app.diagrams.net`
- Use the VS Code extension
- Use the desktop app

Save the file as `architecture.drawio` and include it in your repository.

---

## Required Components

Your diagram must include **all** of the following components:

| Component | Represents |
|-----------|-----------|
| Developer | The person pushing code |
| GitHub Repository | Where source code lives |
| GitHub Actions | The CI/CD automation runner |
| IAM Role (OIDC) | The role assumed via federated identity |
| Amazon S3 | The bucket storing build artifacts |
| Amazon CloudFront | The CDN serving content globally |
| Browser / End Users | The people visiting the website |

---

## Required Flows

Your diagram must clearly show **two distinct flows**:

### Deployment Flow (top to bottom or left to right)
Show how code moves from developer to production:

```
Developer → GitHub Repository → GitHub Actions → IAM Role → S3 Bucket
```

### User Request Flow
Show how a user's browser request is served:

```
Browser → CloudFront → S3 Bucket
```

---

## Diagram Tips

- Use **AWS service icons** where available (Draw.io has an AWS icon library)
- Use **arrows with labels** to indicate the direction and nature of each flow
- Separate the two flows visually (e.g. use different arrow colors or dashed lines)
- Keep it clean and readable — avoid clutter
- Group related components with swimlanes or bounding boxes if helpful

---

## What Makes a Good Diagram

A good architecture diagram tells a story at a glance:
- Someone unfamiliar with the project should understand the flow in 30 seconds
- Every component has a clear role
- Arrows show direction and (ideally) what is being transmitted
- The diagram matches the actual infrastructure you built

---

## Deliverables for This Step

- [ ] `architecture.drawio` file saved in your repository
- [ ] A screenshot of the diagram (PNG or JPEG) to include in your README

---

**Previous:** [Step 10 – Validation](10-validation.md)  
**Next:** [Step 12 – Write the README and Prepare Submission](12-readme-and-submission.md)
