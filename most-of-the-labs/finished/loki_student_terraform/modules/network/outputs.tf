output "vpc_id" {
  description = "Default VPC ID."
  value       = data.aws_vpc.default.id
}

output "subnet_id" {
  description = "First subnet ID from the default VPC."
  value       = data.aws_subnets.default.ids[0]
}
