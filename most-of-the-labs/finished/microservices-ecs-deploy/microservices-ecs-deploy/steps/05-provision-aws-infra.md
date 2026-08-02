# Step 05 — Provision the AWS infrastructure

**Goal:** create, from scratch in the AWS Console, the foundational AWS resources
the ECS services need: the execution role, ECR repos, CloudWatch log groups, ECS
cluster, Service Connect namespace, task definitions, and security groups. You'll
create the services themselves in [Step 06](06-create-ecs-services.md).

Use the **same AWS region** for everything (this lab assumes `eu-west-1`). If you
pick another, use it everywhere — including the workflow `env` in Step 07 and the
`<REGION>` placeholders in the task definitions.

Build the resources in the order below; each is needed by the next.

```
ecsTaskExecutionRole ─┐
ECR repos ────────────┤
CloudWatch log groups ┤──► task definitions ─┐
Cloud Map namespace ──┘                       ├──► (Step 06) ECS services
security groups ──────────────────────────────┘
```

---

## A. Fill in the task-definition placeholders

Edit `inventory-service/task-definition.json` and `orders-service/task-definition.json`
and replace:

- [ ] `<ACCOUNT_ID>` → your 12-digit AWS account ID (e.g. `050752632489`)
- [ ] `<REGION>` → your region, e.g. `eu-west-1`

These appear in `executionRoleArn`, the container `image` URI, and `awslogs-region`.
Leave everything else as-is — the container `name` and `family` are matched by the
pipeline later. The console names below (ECR repo, log group, execution role) must
match this JSON exactly.

---

## B. Create the task execution role

1. Open the **IAM** console → **Roles** → **Create role**.
2. **Trusted entity type:** **AWS service**.
3. **Service or use case:** **Elastic Container Service** → select **Elastic Container Service Task** → **Next**.
4. In **Permissions policies** search `AmazonECSTaskExecutionRolePolicy`, tick it → **Next**.
5. **Role name:** `ecsTaskExecutionRole`. Leave description and trust policy as generated → **Create role**.

---

## C. Create the two ECR repositories

Set the console region selector (top-right) to your `<REGION>` before creating —
repos can't move regions later.

1. Open the **Amazon ECR** console → **Private registry → Repositories**.
2. Click **Create repository**.
3. On the **Create repository** page:
   - **Repository name:** `inventory-service`. Check the URI prefix shows your account ID and region.
   - **Image tag mutability:** **Mutable**.
   - **Encryption configuration:** **AES-256**.
   - Leave remaining sections at defaults.
4. Click **Create repository**.
5. Click **Create repository** again and repeat step 3 with name `orders-service`.

Both repos now show a URI of the form `<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<name>`.

---

## D. Create the two CloudWatch log groups

Set the CloudWatch region selector to the same region as `awslogs-region`.

1. Open the **CloudWatch** console → **Logs → Log groups** → **Create log group**.
2. **Log group name:** `/ecs/inventory-service`. Leave **Log class** **Standard** and **Retention** **Never expire** → **Create**.
3. Click **Create log group** again and repeat with `/ecs/orders-service`.

---

## E. Create the ECS cluster

1. Open the **Amazon ECS** console → **Clusters** → **Create cluster**.
2. **Cluster name:** `microsvc-cluster` (must equal `ECS_CLUSTER` in your Step 07 workflow).
3. **Infrastructure:** leave **AWS Fargate (serverless)** ticked. Leave EC2 and External unticked.
4. Leave Monitoring and Tags at defaults → **Create**. Wait for status **Active**.

---

## F. Create the Cloud Map namespace

1. Open the **AWS Cloud Map** console → **Create namespace**.
2. **Namespace name:** `microsvc.local`. Leave description blank.
3. **Instance discovery:** **API calls and DNS queries in VPCs**.
4. **VPC:** the **default VPC** in your region (same VPC used for both services in Section H).
5. Click **Create namespace**.

---

## G. Register the first task-definition revisions

1. Open the **Amazon ECS** console → **Task definitions**.
2. **Create new task definition** dropdown → **Create new task definition with JSON**.
3. Delete the sample JSON, paste the full contents of `inventory-service/task-definition.json` (placeholders filled in) → **Create**.
4. Repeat for `orders-service/task-definition.json`.

You should now have two families — `inventory-service` and `orders-service` — each at revision `1`.

---

## G2. Create the security groups

Create all three in the **default VPC**, **in this order** — each rule's source group must already exist:

```
internet ──80──► alb-sg ──80──► orders-sg ──8080──► inventory-sg
```

Open **EC2 → Security Groups → Create security group**:

1. **`alb-sg`** — **Description** `ALB inbound from internet`; VPC: default VPC.
   - **Inbound:** **Type** **HTTP**, **Port** `80`, **Source** **Anywhere-IPv4** (`0.0.0.0/0`), **Description** `HTTP from internet`.
   - Leave outbound at default → **Create security group**.

2. **`orders-sg`** — **Description** `orders task, ALB only`; VPC: default VPC.
   - **Inbound:** **Type** **Custom TCP**, **Port** `8080`, **Source** the **`alb-sg`** group, **Description** `8080 from alb-sg` → **Create security group**.

3. **`inventory-sg`** — **Description** `inventory task, orders only`; VPC: default VPC.
   - **Inbound:** **Type** **Custom TCP**, **Port** `8080`, **Source** the **`orders-sg`** group, **Description** `8080 from orders-sg` → **Create security group**.

---

## Checklist

- [ ] (A) `<ACCOUNT_ID>` and `<REGION>` filled into both `task-definition.json` files
- [ ] (B) `ecsTaskExecutionRole` exists with `AmazonECSTaskExecutionRolePolicy`
- [ ] (C) ECR repos `inventory-service` and `orders-service` exist (Private)
- [ ] (D) Log groups `/ecs/inventory-service` and `/ecs/orders-service` exist
- [ ] (E) Cluster `microsvc-cluster` exists on Fargate
- [ ] (F) Cloud Map namespace `microsvc.local` exists in the default VPC
- [ ] (G) A revision of each task definition is registered
- [ ] (G2) Security groups exist: `alb-sg` (80 from `0.0.0.0/0`), `orders-sg` (8080 from `alb-sg`), `inventory-sg` (8080 from `orders-sg`)

## Next

→ [Step 06 — Create the ECS services](06-create-ecs-services.md)
