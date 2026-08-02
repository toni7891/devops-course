# Microservices → ECS/ECR via GitHub Actions (OIDC)

> Take two small, dependent microservices from your laptop all the way to
> **Amazon ECS Fargate** — shipped by a **GitHub Actions** pipeline that
> authenticates to AWS with **OIDC**. **No SSH. No AWS access keys. Ever.**

This is a hands-on lab. You start with two Flask services that talk to each
other, and by the end you have a real, repeatable deploy pipeline pushing them
to AWS on every `git push`.

---

## Why this lab

Most "deploy to the cloud" tutorials stop at a single container behind a load
balancer. Real systems are messier: services depend on each other, secrets leak
when you store long-lived keys, and "it works on my machine" hides deploy bugs.

This lab tackles all three:

- **Service-to-service dependency** — `orders` can't answer a request without
  calling `inventory`. You prove that call works *locally* first, so any later
  failure is a deploy problem, not an app problem.
- **Keyless AWS auth** — GitHub Actions assumes an IAM role via **OIDC**. There
  are no AWS access keys stored as GitHub secrets to leak or rotate.
- **Declarative, idempotent deploys** — each service ships from a templated ECS
  task definition, tagged by commit SHA, through a GitHub Actions matrix.

You learn the same patterns you'd use to run microservices in production — just
scaled down to two services you can hold in your head.

---

## What you'll build

```
git push → GitHub Actions (matrix: inventory, orders)
               │
               ├─ [OIDC → AWS, no stored keys]
               ├─ [docker build + push] ──────→ Amazon ECR (one repo per service)
               └─ [render + deploy task def] ──→ Amazon ECS Fargate
                                                       │
                                          inventory-service   orders-service
                                          (private)           (behind the ALB)
                                                   ▲                  │
                                                   └── Service Connect ┘
                                                                       │
                                                       Application Load Balancer
                                                                       │
                                                       http://<alb-dns-name>/orders
```

`inventory` is never exposed publicly; only `orders` sits behind the load
balancer and reaches `inventory` over a private Service Connect DNS name. The
end-to-end win is hitting the ALB and watching the two services collaborate.

---

## The two services

You're **given** the application code so the lab stays focused on
containerization and deployment — not on writing Flask.

| Service | Endpoint | Behavior |
|---|---|---|
| inventory | `GET /health` | `{"status": "ok"}` |
| inventory | `GET /stock/<sku>` | `{"sku": ..., "quantity": ...}` — `0` for unknown SKUs |
| orders | `GET /health` | `{"status": "ok"}` |
| orders | `POST /orders` `{"sku", "quantity"}` | Calls inventory → `"confirmed"` / `"backordered"`, or `503` if inventory is unreachable |

Each service folder ships its `app.py`, `requirements.txt`, a templated
`task-definition.json`, and tests.

---

## What you write yourself

The instructive parts are left to you:

- A `Dockerfile` for each service → [Step 02](steps/02-containerize.md)
- `docker-compose.yml` to run both together → [Step 03](steps/03-compose-local.md)
- `.github/workflows/deploy.yml`, the OIDC deploy pipeline → [Step 07](steps/07-write-the-pipeline.md)

And you provision **all** the AWS infrastructure yourself from the console —
OIDC trust, ECR, the ECS cluster, Service Connect, and the load balancer
([Step 04](steps/04-github-repo.md) and [Step 05](steps/05-provision-aws-infra.md)).
Nothing is pre-provisioned for you.

---

## The path

Work through these in order — each ends with a checklist; don't move on until it
passes.

| # | Step | What you do |
|---|---|---|
| 1 | [Local development setup](steps/01-local-dev-setup.md) | Create a virtualenv per service, install deps, run the tests |
| 2 | [Containerize each service](steps/02-containerize.md) | Write a `Dockerfile` for inventory and orders |
| 3 | [Run both locally with Compose](steps/03-compose-local.md) | Write `docker-compose.yml`, prove the cross-service call |
| 4 | [Prepare the GitHub repo](steps/04-github-repo.md) | Publish the repo from VS Code; build the OIDC provider + deploy role yourself |
| 5 | [Provision the AWS infrastructure](steps/05-provision-aws-infra.md) | Create the execution role, ECR, log groups, the cluster, Service Connect, task definitions, and security groups |
| 6 | [Create the ECS services](steps/06-create-ecs-services.md) | Create both services and the ALB; wire up Service Connect and the security groups |
| 7 | [Write the deploy pipeline](steps/07-write-the-pipeline.md) | Author `.github/workflows/deploy.yml` (the core exercise) |
| 8 | [Deploy & verify end-to-end](steps/08-deploy-and-verify.md) | Push, watch the run, hit the ALB, prove the dependency |

---

## Concepts covered

| Concept | What you learn |
|---|---|
| Python virtualenvs | Isolated, reproducible per-service dependencies |
| Dockerfiles | Containerizing a Python web service from scratch |
| Docker Compose | Wiring multiple services together for local dev |
| GitHub OIDC | Passwordless AWS auth from GitHub Actions — no stored access keys |
| IAM trust policies | Scoping which repo + branch can assume which role |
| Amazon ECR | Per-service container registries, commit-SHA image tags |
| Amazon ECS Fargate | Serverless container orchestration |
| ECS Service Connect | Service-to-service discovery via a private Cloud Map DNS namespace |
| Render + deploy task definitions | Declarative, idempotent ECS deploys from a JSON template |
| GitHub Actions matrix | Two services deployed independently in the same workflow |
| Application Load Balancer | Only the public-facing service is exposed; the internal one isn't |

---

## Done when

- [ ] A virtualenv exists per service and both test suites pass ([Step 1](steps/01-local-dev-setup.md))
- [ ] You wrote a `Dockerfile` for each service ([Step 2](steps/02-containerize.md))
- [ ] `docker compose up` proves the cross-service call works locally ([Step 3](steps/03-compose-local.md))
- [ ] You built the OIDC provider + deploy role yourself; no AWS access keys as secrets ([Step 4](steps/04-github-repo.md))
- [ ] You provisioned the execution role, ECR, log groups, the cluster, Service Connect, task definitions, and security groups ([Step 5](steps/05-provision-aws-infra.md))
- [ ] You created both ECS services and the ALB ([Step 6](steps/06-create-ecs-services.md))
- [ ] You wrote `.github/workflows/deploy.yml` from scratch ([Step 7](steps/07-write-the-pipeline.md))
- [ ] A push to `main` runs your workflow; both matrix jobs go green independently ([Step 8](steps/08-deploy-and-verify.md))
- [ ] `aws ecs describe-services` shows both services with `running == desired`
- [ ] The ALB returns `confirmed` / `backordered` correctly through the real deployment
