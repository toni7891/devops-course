#!/usr/bin/env bash
#
# aws_resource_scan.sh
# Scans all AWS regions for active resources and pulls a Cost Explorer
# cost-by-service breakdown for the trailing period.
#
# Requires: aws cli v2, jq, valid AWS credentials (profile or env vars).

set -euo pipefail

PROFILE="${AWS_PROFILE:-default}"
DAYS_BACK="${DAYS_BACK:-30}"
OUT_DIR="${OUT_DIR:-./aws_scan_$(date +%Y%m%d_%H%M%S)}"

mkdir -p "$OUT_DIR"

echo "== AWS Resource + Cost Scan =="
echo "Profile: $PROFILE"
echo "Output:  $OUT_DIR"
echo

command -v aws >/dev/null || { echo "aws cli not found"; exit 1; }
command -v jq  >/dev/null || { echo "jq not found"; exit 1; }

aws sts get-caller-identity --profile "$PROFILE" >/dev/null || {
  echo "Cannot authenticate with profile '$PROFILE'"; exit 1;
}

# ---------------------------------------------------------------------------
# 1. Cost Explorer: cost by service (account-wide, not region-scoped — CE is
#    a global/billing API, no per-region endpoint exists)
# ---------------------------------------------------------------------------
END_DATE=$(date -u +%Y-%m-%d)
if date -v-1d >/dev/null 2>&1; then
  START_DATE=$(date -u -v-"${DAYS_BACK}"d +%Y-%m-%d)   # BSD/macOS date
else
  START_DATE=$(date -u -d "-${DAYS_BACK} days" +%Y-%m-%d) # GNU date
fi

echo "-- Cost Explorer: cost by service ($START_DATE -> $END_DATE) --"
aws ce get-cost-and-usage \
  --profile "$PROFILE" \
  --time-period Start="$START_DATE",End="$END_DATE" \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --output json > "$OUT_DIR/cost_by_service.json"

jq -r '
  .ResultsByTime[].Groups[]
  | select((.Metrics.UnblendedCost.Amount | tonumber) > 0)
  | [.Keys[0], .Metrics.UnblendedCost.Amount]
  | @tsv
' "$OUT_DIR/cost_by_service.json" | sort -k2 -nr | column -t -s $'\t' \
  | tee "$OUT_DIR/cost_by_service.txt"

echo
echo "-- Cost Explorer: cost by region --"
aws ce get-cost-and-usage \
  --profile "$PROFILE" \
  --time-period Start="$START_DATE",End="$END_DATE" \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=REGION \
  --output json > "$OUT_DIR/cost_by_region.json"

jq -r '
  .ResultsByTime[].Groups[]
  | select((.Metrics.UnblendedCost.Amount | tonumber) > 0)
  | [.Keys[0], .Metrics.UnblendedCost.Amount]
  | @tsv
' "$OUT_DIR/cost_by_region.json" | sort -k2 -nr | column -t -s $'\t' \
  | tee "$OUT_DIR/cost_by_region.txt"

# ---------------------------------------------------------------------------
# 2. Enumerate regions actually enabled for this account
# ---------------------------------------------------------------------------
echo
echo "-- Enumerating enabled regions --"
REGIONS=$(aws ec2 describe-regions \
  --all-regions \
  --profile "$PROFILE" \
  --query "Regions[?OptInStatus=='opt-in-not-required' || OptInStatus=='opted-in'].RegionName" \
  --output text)

echo "Regions to scan: $REGIONS"
echo

RESOURCE_CSV="$OUT_DIR/active_resources.csv"
echo "region,service,resource_id,extra" > "$RESOURCE_CSV"

scan_region () {
  local region="$1"
  echo "== Region: $region =="

  # EC2 instances (running/stopped)
  aws ec2 describe-instances \
    --profile "$PROFILE" --region "$region" \
    --query "Reservations[].Instances[].[InstanceId,State.Name,InstanceType]" \
    --output text 2>/dev/null | while read -r id state itype; do
      [ -n "${id:-}" ] && echo "$region,ec2_instance,$id,${state}|${itype}" >> "$RESOURCE_CSV"
  done

  # EBS volumes
  aws ec2 describe-volumes \
    --profile "$PROFILE" --region "$region" \
    --query "Volumes[].[VolumeId,State,Size]" \
    --output text 2>/dev/null | while read -r id state size; do
      [ -n "${id:-}" ] && echo "$region,ebs_volume,$id,${state}|${size}GB" >> "$RESOURCE_CSV"
  done

  # RDS instances
  aws rds describe-db-instances \
    --profile "$PROFILE" --region "$region" \
    --query "DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,Engine]" \
    --output text 2>/dev/null | while read -r id status engine; do
      [ -n "${id:-}" ] && echo "$region,rds_instance,$id,${status}|${engine}" >> "$RESOURCE_CSV"
  done

  # Lambda functions
  aws lambda list-functions \
    --profile "$PROFILE" --region "$region" \
    --query "Functions[].[FunctionName,Runtime]" \
    --output text 2>/dev/null | while read -r name runtime; do
      [ -n "${name:-}" ] && echo "$region,lambda_function,$name,${runtime}" >> "$RESOURCE_CSV"
  done

  # Classic + ALB/NLB load balancers
  aws elbv2 describe-load-balancers \
    --profile "$PROFILE" --region "$region" \
    --query "LoadBalancers[].[LoadBalancerName,Type,State.Code]" \
    --output text 2>/dev/null | while read -r name type state; do
      [ -n "${name:-}" ] && echo "$region,elbv2,$name,${type}|${state}" >> "$RESOURCE_CSV"
  done

  # NAT gateways (common hidden cost)
  aws ec2 describe-nat-gateways \
    --profile "$PROFILE" --region "$region" \
    --filter "Name=state,Values=available,pending" \
    --query "NatGateways[].[NatGatewayId,State]" \
    --output text 2>/dev/null | while read -r id state; do
      [ -n "${id:-}" ] && echo "$region,nat_gateway,$id,${state}" >> "$RESOURCE_CSV"
  done

  # Elastic IPs (cost money when unattached)
  aws ec2 describe-addresses \
    --profile "$PROFILE" --region "$region" \
    --query "Addresses[].[AllocationId,AssociationId]" \
    --output text 2>/dev/null | while read -r alloc assoc; do
      [ -n "${alloc:-}" ] && echo "$region,eip,$alloc,${assoc:-unattached}" >> "$RESOURCE_CSV"
  done

  # ECS clusters with running tasks
  aws ecs list-clusters \
    --profile "$PROFILE" --region "$region" \
    --query "clusterArns" --output text 2>/dev/null | tr '\t' '\n' | while read -r arn; do
      [ -n "${arn:-}" ] && echo "$region,ecs_cluster,$arn," >> "$RESOURCE_CSV"
  done
}

for region in $REGIONS; do
  scan_region "$region" &
  # cap parallelism so you don't get throttled
  while [ "$(jobs -r | wc -l)" -ge 6 ]; do wait -n; done
done
wait

# S3 buckets are global-namespace, list once
echo
echo "-- S3 buckets (global) --"
aws s3api list-buckets --profile "$PROFILE" \
  --query "Buckets[].Name" --output text | tr '\t' '\n' | while read -r bucket; do
    [ -n "${bucket:-}" ] && echo "global,s3_bucket,$bucket," >> "$RESOURCE_CSV"
done

echo
echo "== Done =="
echo "Resources: $RESOURCE_CSV"
echo "Cost by service: $OUT_DIR/cost_by_service.txt"
echo "Cost by region:  $OUT_DIR/cost_by_region.txt"
echo
echo "Resource count by region/service:"
tail -n +2 "$RESOURCE_CSV" | cut -d',' -f1,2 | sort | uniq -c | sort -rn
