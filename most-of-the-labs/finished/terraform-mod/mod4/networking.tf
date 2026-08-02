resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  # 10.0.0.1
  # 10.0.255.255

  tags = {
    "Name" = "06-resources-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.0.0/24"
  # 10.0.0.1 -> 10.0.0.255
  availability_zone = "eu-west-1a"
  # eu-west-1a
  # eu-west-1b
  # eu-west-1c

  tags = {
    "Name" = "06-resources-public-subnet"
  }

}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id


  tags = {
    "Name" = "06-resources-igw"
  }
}


resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    "Name" = "06-resources-public-rt"
  }
  # Result: {managed_by: Terraform, project: 06-resources, cost_center: 1234, Name: 06-resources-vpc}
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
