#!/bin/bash

# ── Docker ───────────────────────────────────────────────────────

# Build Docker Image
docker build -t ecr-asg-s-test .

# Build for linux/amd64 (Mac users) and push to ECR
docker buildx build --platform linux/amd64 \
  -t 050752632489.dkr.ecr.us-east-1.amazonaws.com/ecr-asg-s-test:latest \
  --push .

# ── ECR ──────────────────────────────────────────────────────────

# Authenticate Docker with ECR
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin \
      050752632489.dkr.ecr.us-east-1.amazonaws.com

# Tag local image
docker tag ecr-asg-s-test \
  050752632489.dkr.ecr.us-east-1.amazonaws.com/ecr-asg-s-test:latest

# Push image to ECR
docker push 050752632489.dkr.ecr.us-east-1.amazonaws.com/ecr-asg-s-test:latest

# Pull image from ECR
docker pull 050752632489.dkr.ecr.us-east-1.amazonaws.com/ecr-asg-s-test:latest

# Run container from ECR image
docker run -p 3000:3000 \
  050752632489.dkr.ecr.us-east-1.amazonaws.com/ecr-asg-s-test:latest

# ── Stress Tests ─────────────────────────────────────────────────

# CPU stress (requires: brew install hey)
hey -n 500 -c 50 http://<public-ip>:3000/cpu

# Memory stress
hey -n 200 -c 20 http://<public-ip>:3000/memory

# CPU stress (curl fallback)
for i in {1..2000}; do curl -s http://<public-ip>:3000/cpu & done; wait
for i in {1..2000}; do curl -s http://localhost:3000/cpu & done; wait

# Memory stress (curl fallback)
for i in {1..2000}; do curl -s http://<public-ip>:3000/memory & done; wait
for i in {1..2000}; do curl -s http://localhost:3000/memory & done; wait
