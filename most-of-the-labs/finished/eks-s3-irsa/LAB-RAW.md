# Lab: EKS S3 Access — IRSA & Pod Identity

---

## Pre-Lab: Generate Your Configuration Files with AI

Before running any commands, you will create all the configuration files yourself using an AI assistant (Claude, ChatGPT, etc.). This is the skill of **vibe coding** — translating technical requirements into prompts and letting AI generate the files for you.

For each file below, read the specs, write your own prompt to an AI assistant, review the output, then save it to the correct path.

---

### File 1 — `eks.yaml`

- eksctl `ClusterConfig` manifest
- Cluster name: `cluster`, region: `us-east-1`
- Availability zones: `us-east-1a`, `us-east-1b`
- One managed node group: name `on-demand`, type `t2.small`, 1 node, 20GB volume

**Save to:** `eks.yaml`

---

### File 2 — `Makefile`

- Two targets: `create` and `delete`
- Both wrap `eksctl` with `-f eks.yaml`
- Default target runs `create`

**Save to:** `Makefile`

---

### File 3 — `iam-policy.json`

- IAM policy document (JSON)
- Action: `s3:GetObject`
- Resource: all objects inside your S3 bucket

**Save to:** `iam-policy.json`

---

### File 4 — `k8s/sa.yaml`

- Kubernetes `ServiceAccount`
- Name: `app`, namespace: `default`
- Annotation: `eks.amazonaws.com/role-arn` pointing to your IAM Role ARN

**Save to:** `k8s/sa.yaml`

---

### File 5 — `k8s/deployment.yaml`

- Kubernetes `Deployment`, name: `nginx-deployment`, namespace: `default`, 1 replica
- Service account: `app`
- initContainer: image `amazon/aws-cli`, downloads `README.md` from your S3 bucket to stdout
- Main container: `nginx:1.14.2`, port 80

**Save to:** `k8s/deployment.yaml`

---

### File 6 — `pod-identity-trust-policy.json`

- IAM trust policy document (JSON)
- Principal: AWS service `pods.eks.amazonaws.com`
- Actions: `sts:AssumeRole` and `sts:TagSession`

**Save to:** `pod-identity-trust-policy.json`

---

### File 7 — `k8s-pod-identity/sa.yaml`

- Kubernetes `ServiceAccount`
- Name: `app`, namespace: `default`
- No annotations — role binding is managed in AWS, not in the YAML

**Save to:** `k8s-pod-identity/sa.yaml`

---

> **Before moving on:** Verify all 7 files exist, review each one, and replace any placeholder values (`<your-bucket-name>`, `<your-account-id>`) with your real values.

---

## Part 1: IRSA (IAM Roles for Service Accounts)

### Step 1 — Install Prerequisites
Install `make`, `kubectl`, `eksctl`, and AWS CLI. Configure AWS credentials.

### Step 2 — Create the EKS Cluster
Use `make create` to spin up the cluster from `eks.yaml`.

### Step 3 — Create an S3 Bucket
Create a bucket and upload a test file (`README.md`).

### Step 4 — Associate an OIDC Provider
Link an IAM OIDC Identity Provider to the EKS cluster — required for IRSA.

### Step 5 — Create an IAM Policy
Define S3 read permissions using `iam-policy.json`.

### Step 6 — Create an IAM Role
Create a role with a trust policy that allows only the `app` Service Account to assume it via the OIDC provider.

### Step 7 — Create the Kubernetes Service Account
Apply `k8s/sa.yaml` — the Service Account is annotated with the IAM Role ARN.

### Step 8 — Deploy the Application
Apply `k8s/deployment.yaml` — nginx with an `aws-cli` initContainer that downloads the file from S3.

### Step 9 — Verify
Check that the initContainer logs show the file content and nginx reaches `Running` status.

---

## Part 2: Pod Identity

### Step 1 — Install the Pod Identity Agent Addon
Enable the `eks-pod-identity-agent` addon on the cluster — it runs as a DaemonSet on each node.

### Step 2 — Create an IAM Role with Pod Identity Trust Policy
Create a new role using `pod-identity-trust-policy.json` — it trusts `pods.eks.amazonaws.com` instead of the OIDC provider.

### Step 3 — Create a Pod Identity Association
Link the IAM Role to the `app` Service Account in the `default` namespace via the AWS EKS API.

### Step 4 — Remove the SA Annotation
Apply `k8s-pod-identity/sa.yaml` — the Service Account has no IAM role annotation.

### Step 5 — Redeploy and Restart
Apply the updated deployment and restart the pods.

### Step 6 — Verify
Confirm the initContainer still reads from S3 — now via Pod Identity instead of IRSA.
