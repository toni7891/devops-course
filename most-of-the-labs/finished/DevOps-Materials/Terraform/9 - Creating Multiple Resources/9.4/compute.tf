data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_ami" "nginx" {
  most_recent = true
  owners      = ["679593333241"] # Bitnami

  filter {
    name   = "name"
    # Matches the latest 1.29 branch on Debian 12
    values = ["bitnami-nginx-1.29*-debian-12-amd64-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# resource "aws_instance" "from_count" {
#   count         = var.ec2_instance_count
#   ami           = data.aws_ami.ubuntu.id
#   instance_type = "t2.micro"

#   subnet_id = aws_subnet.main[
#     count.index % length(aws_subnet.main)
#   ].id

#   tags = {
#     Name    = "${local.project}-${count.index}"
#     Project = local.project
#   }
# }

resource "aws_instance" "from_list" {
  count = length(var.ec2_instance_config_list)
  ami = local.ami_ids[
    var.ec2_instance_config_list[count.index].ami
  ]
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.main[0].id

  tags = {
    Name    = "${local.project}-0"
    Project = local.project
  }
}
