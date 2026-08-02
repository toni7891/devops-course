# CI/CD Lab Implementation Plan — React/Vite → AWS S3 + CloudFront

## Goal
Automate the DataBite frontend deployment so every push to `main` builds, deploys to S3, and invalidates CloudFront — no manual steps.

---

## Architecture
```
Developer
   ↓ git push → main
GitHub Actions
   ├── build job
   │      ├── npm ci (frontend/)
   │      ├── npm run build  →  frontend/dist/
   │      └── upload artifact: react-vite-build
   └── deploy job  (needs: build)
          ├── download artifact → dist/
          ├── aws s3 sync dist/ s3://BUCKET --delete
          └── aws cloudfront create-invalidation --paths "/*"
                    ↓
          Updated Production Website
```

---

## Files to Create / Modify

| Action | Path |
|--------|------|
| CREATE | `.github/workflows/deploy.yml` |

Everything else (IAM, secrets, domain) is done manually in AWS + GitHub UI.

---

## Checklist

### Manual (student does these in AWS Console + GitHub)
- [ ] Collect S3 bucket name, CloudFront distribution ID, AWS region
- [ ] Create IAM policy `ReactFrontendDeployPolicy` (s3 + cloudfront:CreateInvalidation)
- [ ] Create IAM user `github-actions-react-deployer`, attach policy
- [ ] Generate IAM access keys
- [ ] Add 5 GitHub repository secrets:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`
  - `AWS_S3_BUCKET_NAME`
  - `CLOUDFRONT_DISTRIBUTION_ID`

### Code (Claude implements)
- [x] Create `.github/workflows/deploy.yml`

---

## Workflow Details

### Trigger
- Push to `main` branch only

### Job: `build`
1. `actions/checkout@v4`
2. `actions/setup-node@v4` — Node 22, npm cache (path: `frontend/package-lock.json`)
3. `npm ci` — `working-directory: frontend`
4. `npm run build` — `working-directory: frontend` → outputs `frontend/dist/`
5. `actions/upload-artifact@v4` — name: `react-vite-build`, path: `frontend/dist`

### Job: `deploy` (needs: build)
1. `actions/download-artifact@v4` — name: `react-vite-build`, path: `dist`
2. `aws-actions/configure-aws-credentials@v4` — uses secrets
3. `aws s3 sync dist s3://${{ secrets.AWS_S3_BUCKET_NAME }} --delete`
4. `aws cloudfront create-invalidation --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} --paths "/*"`

---

## Verification Steps
1. Push workflow → GitHub Actions shows 2 jobs running in sequence
2. Build job artifact `react-vite-build` appears in the run
3. Deploy job starts only after build succeeds
4. S3 bucket contains updated files
5. CloudFront invalidation created
6. Production URL updated after hard refresh (CMD+SHIFT+R)
