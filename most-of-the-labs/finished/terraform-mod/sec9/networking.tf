locals {
  project = "09-multipul-resources"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    project = local.project
    Name    = "${local.project}-vpc"
  }
}

# resource "aws_subnet" "main" {
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = "10.0.0.0/24"
#   availability_zone = "us-east-1a"

#   tags = {
#     Name = "public-subnet"
#   }
# }

# resource "aws_subnet" "secondery" {
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = "10.0.0.0/24"
#   availability_zone = "us-east-1a"

#   tags = {
#     Name = "public-subnet"
#   }
# }

resource "aws_subnet" "main" {
  count      = var.subnet_count
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.${count.index}.0/24"


  tags = {
    Name    = "${local.project}-subnet-${count.index}"
    project = local.project
  }
}