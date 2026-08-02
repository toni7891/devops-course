data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

locals {
  loki_user_data = file("${path.module}/templates/loki_server_user_data.sh")

  app_user_data = templatefile("${path.module}/templates/app_node_user_data.sh.tftpl", {
    index_js     = file("${path.root}/app/index.js")
    package_json = file("${path.root}/app/package.json")
  })
}

resource "aws_key_pair" "main" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

resource "aws_instance" "loki" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  key_name                    = aws_key_pair.main.key_name
  vpc_security_group_ids      = var.security_group_ids
  associate_public_ip_address = var.associate_public_ip

  user_data                   = local.loki_user_data
  user_data_replace_on_change = true

  tags = {
    Name = var.loki_instance_name
    Role = "loki-server"
  }
}

resource "aws_instance" "nodes" {
  count                       = var.app_node_count
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  key_name                    = aws_key_pair.main.key_name
  vpc_security_group_ids      = var.security_group_ids
  associate_public_ip_address = var.associate_public_ip

  user_data                   = local.app_user_data
  user_data_replace_on_change = true

  tags = {
    Name = "${var.app_node_name_prefix}-${count.index + 1}"
    Role = "app-node"
  }
}
