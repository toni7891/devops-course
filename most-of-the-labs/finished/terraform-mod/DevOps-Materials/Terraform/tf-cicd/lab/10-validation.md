# Step 10 – Validate the Full Deployment

## Goal

Verify that every component of the solution works correctly end-to-end.

---

## Validation Checklist

Work through each section below. Do not skip any — the goal is to confirm that the *whole system* functions as designed, not just individual parts.

---

## 1. Terraform Infrastructure

- [ ] `terraform plan` shows no unexpected changes after the initial apply
- [ ] The S3 bucket exists in the correct region
- [ ] Public access is fully blocked on the bucket (verify in the AWS Console under **Block Public Access settings**)
- [ ] The CloudFront distribution is in **Deployed** status
- [ ] The distribution's origin is the S3 bucket's regional endpoint (not a website endpoint)
- [ ] OAC is associated with the origin (not OAI)

---

## 2. Application Is Accessible via CloudFront

- [ ] Open the CloudFront domain name from your Terraform outputs in a browser
- [ ] The React application loads correctly
- [ ] The browser address bar shows the CloudFront URL (e.g. `https://abcdef123.cloudfront.net`)
- [ ] The connection is served over **HTTPS**

> If you see an "Access Denied" XML error from S3, the bucket policy is not correct.  
> If you see a 403 from CloudFront, check that the default root object is set to `index.html`.

---

## 3. GitHub Actions Pipeline Runs Successfully

- [ ] Push a commit to the `main` branch
- [ ] Go to the **Actions** tab in your GitHub repository
- [ ] The workflow run appears and all steps are green
- [ ] The **Upload to S3** step shows files being transferred
- [ ] The **Invalidate CloudFront Cache** step completes without error
- [ ] Take a screenshot of the successful run — you will need this for submission

---

## 4. Application Updates Automatically

Make a visible change to the React application:
- Change some text in the UI (e.g. a heading or paragraph)
- Commit and push to `main`
- Wait for the GitHub Actions workflow to complete
- Hard-refresh the browser (Ctrl+Shift+R / Cmd+Shift+R) to bypass browser cache
- Confirm the change is visible at the CloudFront URL

> If the change doesn't appear immediately, the CloudFront cache may not have been invalidated yet. Wait a minute and refresh again.

---

## 5. Cache Invalidation Confirms Fresh Content

- In the AWS Console, navigate to your CloudFront distribution
- Go to the **Invalidations** tab
- Confirm that an invalidation was created during the last pipeline run
- Its status should be **Completed**

---

## Common Issues and How to Debug Them

| Symptom | Likely Cause | Where to Look |
|---------|-------------|---------------|
| `AccessDenied` from S3 | Bucket policy missing or incorrect | S3 → Bucket Policy; CloudFront origin settings |
| 403 from CloudFront | Default root object not set | CloudFront distribution settings |
| Stale content after deploy | Cache not invalidated | CloudFront → Invalidations tab |
| GitHub Actions auth failure | OIDC role trust policy too restrictive | IAM Role → Trust relationships |
| `NoSuchBucket` error in workflow | Wrong bucket name in secret | GitHub → Settings → Secrets |
| Pipeline doesn't trigger | Workflow trigger not set to push on `main` | `.github/workflows/deploy.yml` |

---

## Check

Before moving on, confirm:

- [ ] Application loads via CloudFront URL
- [ ] Pipeline ran end-to-end without errors
- [ ] A visible change to the app was deployed automatically
- [ ] Screenshot of successful pipeline is saved
- [ ] CloudFront invalidation is visible in the Console

---

**Previous:** [Step 09 – GitHub Actions Workflow](09-github-actions-workflow.md)  
**Next:** [Step 11 – Create the Architecture Diagram](11-architecture-diagram.md)
