# MERN Stack on AWS EKS — Deployment Guide

## Prerequisites

- EKS cluster already running (`eksctl` or Terraform)
- `kubectl` configured: `aws eks update-kubeconfig --region <REGION> --name <CLUSTER_NAME>`
- `helm` v3 installed
- AWS CLI configured with sufficient permissions
- A domain name with a Route53 hosted zone

---

## Step 1 — Replace Placeholders

Before applying anything, do a find-replace across `k8s/`:

| Placeholder | Replace with |
|-------------|--------------|
| `<ACCOUNT_ID>` | Your 12-digit AWS account ID |
| `<REGION>` | AWS region (e.g. `us-east-1`) |
| `<CLUSTER_NAME>` | Your EKS cluster name |
| `YOUR_DOMAIN` | Your domain (e.g. `example.com`) |
| `your-email@example.com` | Your email for Let's Encrypt |

---

## Step 2 — Install AWS Load Balancer Controller

```bash
# Create IAM policy (one-time)
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam_policy.json

# Create IRSA role (replace placeholders)
eksctl create iamserviceaccount \
  --cluster=<CLUSTER_NAME> \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --attach-policy-arn=arn:aws:iam::<ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
  --override-existing-serviceaccounts \
  --approve

# Install via Helm
helm repo add eks https://aws.github.io/eks-charts
helm repo update
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  --namespace kube-system \
  -f k8s/aws-load-balancer-controller/values.yaml

# Verify
kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller
```

---

## Step 3 — Install External DNS

```bash
# Create IRSA role with Route53 permissions
eksctl create iamserviceaccount \
  --cluster=<CLUSTER_NAME> \
  --namespace=kube-system \
  --name=external-dns \
  --attach-policy-arn=arn:aws:iam::aws:policy/AmazonRoute53FullAccess \
  --override-existing-serviceaccounts \
  --approve

# Install via Helm
helm repo add external-dns https://kubernetes-sigs.github.io/external-dns/
helm repo update
helm install external-dns external-dns/external-dns \
  --namespace kube-system \
  -f k8s/external-dns/values.yaml

# Verify
kubectl get pods -n kube-system -l app.kubernetes.io/name=external-dns
```

---

## Step 4 — Install cert-manager

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true

# Verify
kubectl get pods -n cert-manager

# Apply ClusterIssuers (staging first to test — no rate limits)
kubectl apply -f k8s/cert-manager/cluster-issuer.yaml
kubectl get clusterissuer
```

---

## Step 5 — Apply Namespace and Secrets

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Encode your real values
echo -n 'mongodb://mongodb:27017/ordersdb' | base64
echo -n 'your-super-secret-jwt-key' | base64

# Edit k8s/secrets.yaml — paste the base64 values, then apply
kubectl apply -f k8s/secrets.yaml

# Verify
kubectl get secret app-secrets -n orders-app
```

---

## Step 6 — Deploy MongoDB, Backend, Frontend

```bash
# MongoDB (order matters: PV → PVC → Deployment → Service)
kubectl apply -f k8s/mongo/pv.yaml
kubectl apply -f k8s/mongo/pvc.yaml
kubectl apply -f k8s/mongo/deployment.yaml
kubectl apply -f k8s/mongo/service.yaml

# Backend
kubectl apply -f k8s/backend/deployment.yaml
kubectl apply -f k8s/backend/service.yaml

# Frontend
kubectl apply -f k8s/frontend/deployment.yaml
kubectl apply -f k8s/frontend/service.yaml

# Check all pods are Running
kubectl get pods -n orders-app
```

---

## Step 7 — Apply Ingress

```bash
# Make sure YOUR_DOMAIN is replaced in ingress.yaml first
kubectl apply -f k8s/ingress.yaml

# Watch ALB provisioning (takes ~2 min)
kubectl get ingress -n orders-app -w
```

---

## Step 8 — Verify Everything

```bash
# All pods Running
kubectl get pods -n orders-app

# Services
kubectl get svc -n orders-app

# Ingress — ADDRESS column should show ALB DNS name
kubectl get ingress -n orders-app

# Check certificate issued
kubectl get certificate -n orders-app
kubectl describe certificate -n orders-app

# Check DNS propagated (replace YOUR_DOMAIN)
dig orders.YOUR_DOMAIN

# Smoke test
curl https://orders.YOUR_DOMAIN/api/health
curl https://orders.YOUR_DOMAIN
```

### Troubleshooting

```bash
# Pod logs
kubectl logs -n orders-app deployment/backend
kubectl logs -n orders-app deployment/frontend
kubectl logs -n orders-app deployment/mongodb

# Describe for events
kubectl describe pod -n orders-app -l app=backend

# cert-manager logs
kubectl logs -n cert-manager deployment/cert-manager

# ALB controller logs
kubectl logs -n kube-system deployment/aws-load-balancer-controller
```
