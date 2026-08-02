# Step 04 – Provision the S3 Bucket

## Goal

Create the S3 bucket that will store your React application's build files, and configure it correctly for use with CloudFront.

---

## Background

When hosting a static website with CloudFront + S3, the S3 bucket should **not** be publicly accessible on its own.  
Instead, CloudFront will be granted exclusive access to the bucket using **Origin Access Control (OAC)**.

This means:
- Public access to the bucket is **blocked**
- The bucket does **not** need static website hosting enabled
- Only CloudFront can read the objects

---

## Tasks

### 1. Create the S3 Bucket

Define an `aws_s3_bucket` resource using the bucket name from your variables.

> Think about: should you use `force_destroy = true` during the lab? What does that option do?

---

### 2. Enable Bucket Versioning

Add an `aws_s3_bucket_versioning` resource linked to your bucket.

Versioning keeps a history of every file uploaded.

> Why might versioning be useful for a static website? What are the trade-offs?

---

### 3. Block All Public Access

Add an `aws_s3_bucket_public_access_block` resource.

Make sure **all four** block settings are enabled.

> Why is it important to block public access when using CloudFront with OAC?

---

### 4. Create a Bucket Policy

The bucket policy will allow CloudFront to perform `s3:GetObject` on your bucket.

This policy will reference the CloudFront distribution's ARN — but you haven't created CloudFront yet.

> For now, think about the **structure** of this policy:
> - What principal should be allowed?
> - What action is needed?
> - What resource does it apply to?
> - What condition ties it to a specific CloudFront distribution?

You will wire up the actual CloudFront ARN in the next step. For now, add a placeholder or leave this resource for after you create the CloudFront distribution.

---

### 5. Tag Your Resources

Add consistent tags to your bucket resources.

> Suggested tags: `Name`, `Environment`, `Project`, `ManagedBy`

---

## Key Concepts

- `aws_s3_bucket` creates the bucket itself.
- `aws_s3_bucket_versioning` is a **separate resource** that must reference the bucket.
- `aws_s3_bucket_public_access_block` is also separate — do not confuse it with the bucket ACL.
- Bucket policies use IAM JSON syntax.

---

## Check

Before moving on, confirm:

- [ ] Bucket name comes from a variable (not hardcoded)
- [ ] Public access is fully blocked
- [ ] Versioning is enabled
- [ ] You understand what the bucket policy needs to contain (even if not finished yet)

---

**Previous:** [Step 03 – Provider and Variables](03-terraform-provider-and-variables.md)  
**Next:** [Step 05 – Provision CloudFront with Origin Access Control](05-terraform-cloudfront.md)
