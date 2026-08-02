# Instructor commands — AWS infra, GitHub wiring, verification, teardown

Instructor-only. Not shipped to students. Plain `aws`/`gh` CLI, no Terraform.
Run every block in order, in a shell that has `aws` (v2, authenticated) and
`gh` (authenticated) on PATH. Re-export the variables block in every new
shell session before running later sections.

---

## 0. Variables

```bash
export AWS_REGION=eu-west-1
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export GITHUB_REPO="ORG/REPO"            # dedicated lab repo, e.g. iitc-college/microservices-ecs-deploy
export CLUSTER_NAME=microsvc-cluster
export NAMESPACE=microsvc.local
```

---

## 1. Networking — default VPC + security groups

```bash
export VPC_ID=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true \
  --region $AWS_REGION --query 'Vpcs[0].VpcId' --output text)

export SUBNET_IDS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC_ID \
  --region $AWS_REGION --query 'Subnets[].SubnetId' --output text)
export SUBNET_CSV=$(echo $SUBNET_IDS | tr ' ' ',')

export ALB_SG_ID=$(aws ec2 create-security-group --group-name microsvc-alb-sg \
  --description "ALB ingress for microsvc lab" --vpc-id $VPC_ID \
  --region $AWS_REGION --query GroupId --output text)
aws ec2 authorize-security-group-ingress --group-id $ALB_SG_ID \
  --protocol tcp --port 80 --cidr 0.0.0.0/0 --region $AWS_REGION

export APP_SG_ID=$(aws ec2 create-security-group --group-name microsvc-sg \
  --description "Service-to-service and ALB ingress for microsvc lab" --vpc-id $VPC_ID \
  --region $AWS_REGION --query GroupId --output text)
aws ec2 authorize-security-group-ingress --group-id $APP_SG_ID \
  --protocol tcp --port 8080 --source-group $APP_SG_ID --region $AWS_REGION
aws ec2 authorize-security-group-ingress --group-id $APP_SG_ID \
  --protocol tcp --port 8080 --source-group $ALB_SG_ID --region $AWS_REGION
```

---

## 2. ALB — internet-facing, fronts `orders` only

```bash
export ALB_ARN=$(aws elbv2 create-load-balancer --name microsvc-alb \
  --type application --subnets $SUBNET_IDS --security-groups $ALB_SG_ID \
  --region $AWS_REGION --query 'LoadBalancers[0].LoadBalancerArn' --output text)

export ALB_DNS=$(aws elbv2 describe-load-balancers --load-balancer-arns $ALB_ARN \
  --region $AWS_REGION --query 'LoadBalancers[0].DNSName' --output text)

export TG_ARN=$(aws elbv2 create-target-group --name microsvc-orders-tg \
  --protocol HTTP --port 8080 --vpc-id $VPC_ID --target-type ip \
  --health-check-path /health --region $AWS_REGION \
  --query 'TargetGroups[0].TargetGroupArn' --output text)

aws elbv2 create-listener --load-balancer-arn $ALB_ARN --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn=$TG_ARN --region $AWS_REGION
```

Inventory gets no target group and no listener — it is never reachable from
the public internet, only from `orders` over Service Connect.

---

## 3. ECR — one repo per service

```bash
aws ecr create-repository --repository-name inventory-service --region $AWS_REGION
aws ecr create-repository --repository-name orders-service --region $AWS_REGION
```

---

## 4. ECS cluster + Service Connect namespace

```bash
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $AWS_REGION

aws servicediscovery create-private-dns-namespace --name $NAMESPACE --vpc $VPC_ID \
  --region $AWS_REGION
# wait ~10s for the create-namespace operation to finish, then resolve its id:
export NAMESPACE_ID=$(aws servicediscovery list-namespaces --region $AWS_REGION \
  --query "Namespaces[?Name=='$NAMESPACE'].Id" --output text)
```

---

## 5. Task execution role + log groups

```bash
cat > /tmp/ecs-trust-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "ecs-tasks.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
EOF

aws iam create-role --role-name ecsTaskExecutionRole \
  --assume-role-policy-document file:///tmp/ecs-trust-policy.json
aws iam attach-role-policy --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

aws logs create-log-group --log-group-name /ecs/inventory-service --region $AWS_REGION
aws logs create-log-group --log-group-name /ecs/orders-service --region $AWS_REGION
```

---

## 6. Register the initial task definitions

Fills `<ACCOUNT_ID>` / `<REGION>` placeholders from the committed
`task-definition.json` files and registers them.

```bash
sed -e "s/<ACCOUNT_ID>/$ACCOUNT_ID/g" -e "s/<REGION>/$AWS_REGION/g" \
  microservices-ecs-deploy/inventory-service/task-definition.json > /tmp/inventory-task-def.json
aws ecs register-task-definition --cli-input-json file:///tmp/inventory-task-def.json \
  --region $AWS_REGION

sed -e "s/<ACCOUNT_ID>/$ACCOUNT_ID/g" -e "s/<REGION>/$AWS_REGION/g" \
  microservices-ecs-deploy/orders-service/task-definition.json > /tmp/orders-task-def.json
aws ecs register-task-definition --cli-input-json file:///tmp/orders-task-def.json \
  --region $AWS_REGION
```

The GitHub Actions deploy re-registers both on every push — this is only to
get the services off the ground.

---

## 7. ECS services — Fargate, Service Connect

`inventory-service` advertises itself as `inventory.microsvc.local:8080`
(server side). `orders-service` resolves it (client side) and is the only
service attached to the ALB target group.

```bash
aws ecs create-service \
  --cluster $CLUSTER_NAME \
  --service-name inventory-service \
  --task-definition inventory-service \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_CSV],securityGroups=[$APP_SG_ID],assignPublicIp=ENABLED}" \
  --service-connect-configuration "{
    \"enabled\": true,
    \"namespace\": \"$NAMESPACE_ID\",
    \"services\": [{
      \"portName\": \"inventory\",
      \"discoveryName\": \"inventory\",
      \"clientAliases\": [{ \"port\": 8080, \"dnsName\": \"inventory\" }]
    }]
  }" \
  --region $AWS_REGION

aws ecs create-service \
  --cluster $CLUSTER_NAME \
  --service-name orders-service \
  --task-definition orders-service \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_CSV],securityGroups=[$APP_SG_ID],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=$TG_ARN,containerName=orders,containerPort=8080" \
  --service-connect-configuration "{ \"enabled\": true, \"namespace\": \"$NAMESPACE_ID\" }" \
  --region $AWS_REGION
```

Wait for both to reach steady state:

```bash
aws ecs wait services-stable --cluster $CLUSTER_NAME \
  --services inventory-service orders-service --region $AWS_REGION
```

---

## 8. GitHub OIDC provider + deploy role

```bash
THUMBPRINT=$(echo | openssl s_client -servername token.actions.githubusercontent.com \
  -connect token.actions.githubusercontent.com:443 2>/dev/null \
  | openssl x509 -fingerprint -sha1 -noout | sed 's/.*=//;s/://g')

aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list "$THUMBPRINT"
```

> AWS no longer actually validates this thumbprint for GitHub's provider, but
> the API still requires a value — any well-formed SHA1 hex string works. If
> an OIDC provider for `token.actions.githubusercontent.com` already exists
> in this account (e.g. from another lab), skip this step and reuse it.

```bash
cat > /tmp/deploy-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Federated": "arn:aws:iam::$ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com" },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" },
      "StringLike": { "token.actions.githubusercontent.com:sub": "repo:$GITHUB_REPO:ref:refs/heads/main" }
    }
  }]
}
EOF

aws iam create-role --role-name github-actions-ecs-deploy \
  --assume-role-policy-document file:///tmp/deploy-trust-policy.json

cat > /tmp/deploy-permissions-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": ["ecr:GetAuthorizationToken"], "Resource": "*" },
    { "Effect": "Allow", "Action": [
        "ecr:BatchCheckLayerAvailability","ecr:InitiateLayerUpload","ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload","ecr:PutImage","ecr:BatchGetImage"
      ], "Resource": [
        "arn:aws:ecr:$AWS_REGION:$ACCOUNT_ID:repository/inventory-service",
        "arn:aws:ecr:$AWS_REGION:$ACCOUNT_ID:repository/orders-service"
      ] },
    { "Effect": "Allow", "Action": [
        "ecs:DescribeServices","ecs:DescribeTaskDefinition",
        "ecs:RegisterTaskDefinition","ecs:UpdateService"
      ], "Resource": "*" },
    { "Effect": "Allow", "Action": ["iam:PassRole"],
      "Resource": "arn:aws:iam::$ACCOUNT_ID:role/ecsTaskExecutionRole" }
  ]
}
EOF

aws iam put-role-policy --role-name github-actions-ecs-deploy \
  --policy-name github-actions-ecs-deploy-policy \
  --policy-document file:///tmp/deploy-permissions-policy.json

export DEPLOY_ROLE_ARN=$(aws iam get-role --role-name github-actions-ecs-deploy \
  --query 'Role.Arn' --output text)
echo "$DEPLOY_ROLE_ARN"
```

---

## 9. Wire the GitHub repo

No AWS access keys — only the role ARN, which is not a secret:

```bash
gh variable set AWS_DEPLOY_ROLE_ARN -b "$DEPLOY_ROLE_ARN" --repo $GITHUB_REPO
```

Copy `solution/.github/workflows/deploy.yml` into `.github/workflows/` at the
root of `$GITHUB_REPO`, and confirm its `env.AWS_REGION` / `env.ECS_CLUSTER`
match the values used above before pushing.

---

## 10. Verify end-to-end

```bash
git push origin main
gh run watch --repo $GITHUB_REPO

aws ecs describe-services --cluster $CLUSTER_NAME \
  --services inventory-service orders-service --region $AWS_REGION \
  --query 'services[].{name:serviceName,running:runningCount,desired:desiredCount}'

curl -sX POST "http://$ALB_DNS/orders" -H 'content-type: application/json' \
  -d '{"sku":"widget","quantity":2}'     # expect status "confirmed"
curl -sX POST "http://$ALB_DNS/orders" -H 'content-type: application/json' \
  -d '{"sku":"gadget","quantity":2}'     # expect status "backordered"
```

Optional dependency proof:

```bash
aws ecs update-service --cluster $CLUSTER_NAME --service inventory-service \
  --desired-count 0 --region $AWS_REGION

curl -sX POST "http://$ALB_DNS/orders" -H 'content-type: application/json' \
  -d '{"sku":"widget","quantity":1}'     # expect 503 inventory service unavailable

aws ecs update-service --cluster $CLUSTER_NAME --service inventory-service \
  --desired-count 1 --region $AWS_REGION
```

---

## 11. Teardown

Run after validating, to stop charges. ALB + 2 Fargate tasks cost a few
cents/hour — don't leave this running between class sessions.

```bash
aws ecs update-service --cluster $CLUSTER_NAME --service inventory-service \
  --desired-count 0 --region $AWS_REGION
aws ecs update-service --cluster $CLUSTER_NAME --service orders-service \
  --desired-count 0 --region $AWS_REGION
aws ecs delete-service --cluster $CLUSTER_NAME --service inventory-service --region $AWS_REGION
aws ecs delete-service --cluster $CLUSTER_NAME --service orders-service --region $AWS_REGION

aws elbv2 describe-listeners --load-balancer-arn $ALB_ARN --region $AWS_REGION \
  --query 'Listeners[].ListenerArn' --output text | xargs -n1 -I{} \
  aws elbv2 delete-listener --listener-arn {} --region $AWS_REGION
aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN --region $AWS_REGION
aws elbv2 delete-target-group --target-group-arn $TG_ARN --region $AWS_REGION

aws servicediscovery delete-namespace --id $NAMESPACE_ID --region $AWS_REGION
aws ecs delete-cluster --cluster $CLUSTER_NAME --region $AWS_REGION

aws ecr delete-repository --repository-name inventory-service --force --region $AWS_REGION
aws ecr delete-repository --repository-name orders-service --force --region $AWS_REGION

aws iam delete-role-policy --role-name github-actions-ecs-deploy \
  --policy-name github-actions-ecs-deploy-policy
aws iam delete-role --role-name github-actions-ecs-deploy
aws iam detach-role-policy --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
aws iam delete-role --role-name ecsTaskExecutionRole

aws ec2 delete-security-group --group-id $APP_SG_ID --region $AWS_REGION
aws ec2 delete-security-group --group-id $ALB_SG_ID --region $AWS_REGION

# Only if no other repo/lab uses this account's GitHub OIDC provider:
aws iam delete-open-id-connect-provider \
  --open-id-connect-provider-arn arn:aws:iam::$ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com
```
