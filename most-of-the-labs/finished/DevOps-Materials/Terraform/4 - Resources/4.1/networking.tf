resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    "Name"       = "06-resources-vpc"
    "managed_by" = "Terraform"
    "project"    = "06-resources"
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = "eu-west-1a"

  tags = {
    "Name"       = "06-resources-public-subnet"
    "managed_by" = "Terraform"
    "project"    = "06-resources"
  }
}
