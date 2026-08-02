resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name    = local.project
    Project = local.project
  }
}

# resource "aws_subnet" "main" {
#   vpc_id     = aws_vpc.main.id
#   cidr_block = "10.0.0.0/24"

#   tags = {
#     Project = local.project
#     Name    = "${local.project}-0"
#   }
# }

# resource "aws_subnet" "secondary" {
#   vpc_id     = aws_vpc.main.id
#   cidr_block = "10.0.1.0/24"

#   tags = {
#     Project = local.project
#     Name    = "${local.project}-1"
#   }
# }

resource "aws_subnet" "main" {
  count  = var.subnet_count
  vpc_id = aws_vpc.main.id
  # cidr_block = "10.0.0.0/24" #! Can't use dynamic block index in terraform configuration file, got error: Error executing plan due to an unexpected resource count (2 expected but only one found) at /home/user/.terraform.d/plugins/darwin_amd64/hashicorp_provider-aws/_registry.tf
  cidr_block = "10.0.${count.index}.0/24"

  tags = {
    Project = local.project
    # Name    = local.project #! Can't use dynamic block index in terraform configuration file, got error: Error executing plan due to an unexpected resource count (2 expected but only one found) at /home/user/.terraform.d/plugins/darwin_amd64/hashicorp_provider-aws/_registry.tf
    Name = "${local.project}-${count.index}"
  }
}