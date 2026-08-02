# Step 05 – Provision CloudFront with Origin Access Control

## Goal

Create a CloudFront distribution that serves your React application from S3, using Origin Access Control (OAC) to keep the bucket private.

---

## Background

**CloudFront** is AWS's Content Delivery Network (CDN). It caches your content at edge locations around the world, so users get fast load times regardless of their location.

**Origin Access Control (OAC)** is the modern, recommended way to connect CloudFront to a private S3 bucket. It replaces the older Origin Access Identity (OAI) approach.

With OAC:
- S3 stays private (no public access)
- CloudFront signs every request to S3
- The bucket policy grants access only to that specific CloudFront distribution

---

## Tasks

### 1. Create the Origin Access Control

Define an `aws_cloudfront_origin_access_control` resource.

You need to specify:
- A name for the OAC
- The origin type (what kind of origin is S3?)
- The signing behavior (should every request be signed?)
- The signing protocol

> Look up the accepted values for each of these settings in the Terraform AWS provider documentation.

---

### 2. Create the CloudFront Distribution

Define an `aws_cloudfront_distribution` resource.

Key settings to configure:

**Origin block:**
- The domain name must point to your S3 bucket's **regional endpoint** (not the website endpoint)
- Attach the OAC you created above using its ID
- Give the origin a unique ID (used to link the origin to cache behaviors)

**Default cache behavior:**
- Set the allowed HTTP methods
- Reference the origin ID you defined
- Choose a viewer protocol policy (should users be forced to use HTTPS?)
- Choose a caching policy or configure TTL values

**Default root object:**
- What file should CloudFront serve when a user visits the root URL `/`?

**Geographic restrictions:**
- For this lab, no restrictions are needed

**Viewer certificate:**
- Use the default CloudFront certificate (no custom domain required)

**Enabled:**
- Make sure the distribution is enabled

> A CloudFront distribution takes several minutes to deploy after `terraform apply`. This is normal.

---

### 3. Complete the S3 Bucket Policy

Now that you have your CloudFront distribution resource, go back to your S3 bucket policy from the previous step.

The policy should:
- Allow the `s3:GetObject` action
- Apply to all objects in your bucket (`arn:aws:s3:::your-bucket-name/*`)
- Grant access only to the CloudFront service principal
- Include a condition that ties the policy to your specific distribution's ARN

> Use Terraform references (`resource.type.name.attribute`) to avoid hardcoding ARNs.

---

### 4. Tag Your Resources

Add consistent tags to the CloudFront distribution.

> Note: CloudFront uses a `tags` map at the top level of the distribution resource, not inside nested blocks.

---

## Key Concepts

- OAC is **not** the same as OAI — make sure you're using the correct resource type.
- The S3 origin domain must use the **regional** format (`bucket.s3.region.amazonaws.com`), not the website hosting endpoint.
- The bucket policy and CloudFront distribution create a **circular dependency** in concept — Terraform handles this because you reference one resource from the other.
- CloudFront distributions have a **status** that changes from `InProgress` to `Deployed`. You can check this in the AWS Console.

---

## Check

Before moving on, confirm:

- [ ] OAC resource is defined and linked to the distribution
- [ ] Distribution origin points to the S3 regional endpoint
- [ ] Default root object is set to `index.html`
- [ ] Viewer protocol policy redirects HTTP to HTTPS
- [ ] S3 bucket policy grants CloudFront access using the distribution ARN
- [ ] All resources are tagged

---

**Previous:** [Step 04 – Provision the S3 Bucket](04-terraform-s3-bucket.md)  
**Next:** [Step 06 – Define Terraform Outputs](06-terraform-outputs.md)
