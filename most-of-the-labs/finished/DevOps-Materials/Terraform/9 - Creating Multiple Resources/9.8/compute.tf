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

resource "aws_instance" "from_map" {
  for_each      = var.ec2_instance_config_map
  ami           = local.ami_ids[each.value.ami]
  instance_type = each.value.instance_type

  subnet_id = aws_subnet.main[each.value.subnet_name].id

  tags = {
    Name    = "${local.project}-${each.key}"
    Project = local.project
  }
}

resource "aws_instance" "from_list" {
  count         = length(var.ec2_instance_config_list)
  ami           = local.ami_ids[var.ec2_instance_config_list[count.index].ami]
  instance_type = var.ec2_instance_config_list[count.index].instance_type

  subnet_id = aws_subnet.main[
    var.ec2_instance_config_list[count.index].subnet_name
  ].id

  tags = {
    Name    = "${local.project}-${count.index}"
    Project = local.project
  }
}
