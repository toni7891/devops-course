output "ubuntu_ami_data_eu" {
  value = data.aws_ami.ubuntu.id
}

# output "aws_caller_identity" {
#   value = data.aws_caller_identity.current
# }

# output "aws_region" {
#   value = data.aws_region.current
# }

# output "us_east_region" {
#   value = data.aws_region.us_east
# }

# output "ubuntu_ami_data_us" {
#   value = data.aws_ami.ubuntu_us.id
# }

output "prod_vpc_id" {
  value = data.aws_vpc.prod_vpc.id
}