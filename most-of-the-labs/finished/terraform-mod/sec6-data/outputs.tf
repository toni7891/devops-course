output "ubuntu_ami_data" {
  value = data.aws_ami.ubuntu.id
}

output "aws_caller_identity" {
  value = data.aws_caller_identity.current
}

output "aws_region" {
  value = data.aws_region.current
}


data "aws_region" "us_east" {
  provider = aws.us_east
}

output "us_east_region" {
  value = data.aws_region.us_east
}

data "aws_vpc" "prod_vpc" {
  tags = {
    Env = "Prod"
  }
}

output "prod_vpc_id" {
  value = data.aws_vpc.prod_vpc.id
}