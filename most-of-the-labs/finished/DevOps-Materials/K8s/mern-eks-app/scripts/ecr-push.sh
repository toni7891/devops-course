#!/usr/bin/env bash
set -euo pipefail

# Detect AWS account + region from current CLI config
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

IMAGES=("backend" "frontend")
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Account : $AWS_ACCOUNT_ID"
echo "Region  : $AWS_REGION"
echo "Registry: $ECR_REGISTRY"
echo ""

# Create ECR repos (skip if already exist)
for IMAGE in "${IMAGES[@]}"; do
  echo "→ Creating ECR repo: $IMAGE"
  aws ecr describe-repositories --repository-names "$IMAGE" --region "$AWS_REGION" > /dev/null 2>&1 || \
    aws ecr create-repository \
      --repository-name "$IMAGE" \
      --region "$AWS_REGION" \
      --image-scanning-configuration scanOnPush=true \
      --query 'repository.repositoryUri' \
      --output text
done

echo ""
echo "→ Authenticating Docker with ECR"
aws ecr get-login-password --region "$AWS_REGION" | \
  docker login --username AWS --password-stdin "$ECR_REGISTRY"

echo ""
# Build, tag, push
for IMAGE in "${IMAGES[@]}"; do
  LOCAL_TAG="mern-eks-app-${IMAGE}:latest"
  REMOTE_TAG="${ECR_REGISTRY}/${IMAGE}:latest"

  echo "→ Building $IMAGE"
  docker buildx build --platform linux/amd64 -t "$LOCAL_TAG" "$PROJECT_ROOT/$IMAGE"

  echo "→ Tagging  $LOCAL_TAG → $REMOTE_TAG"
  docker tag "$LOCAL_TAG" "$REMOTE_TAG"

  echo "→ Pushing  $REMOTE_TAG"
  docker push "$REMOTE_TAG"

  echo "   ✓ $REMOTE_TAG"
  echo ""
done

echo "Done. Images pushed:"
for IMAGE in "${IMAGES[@]}"; do
  echo "  ${ECR_REGISTRY}/${IMAGE}:latest"
done
