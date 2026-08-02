resource "aws_instance" "from_list" {
  count = length(var.ec2_instance_config_list)

  ami = local.ami_ids[
    var.ec2_instance_config_list[count.index].ami
  ]

  instance_type = var.ec2_instance_config_list[count.index].instance_type

  subnet_id = aws_subnet.main[
    count.index % length(aws_subnet.main)
  ].id

  user_data = var.ec2_instance_config_list[count.index].ami == "nginx" ? local.nginx_user_data : null

  tags = {
    Name    = "${local.project}-${count.index}"
    Project = local.project
  }
}

locals {
  ami_ids = {
    ubuntu = data.aws_ami.ubuntu.id
    nginx  = data.aws_ami.nginx.id
  }

  nginx_user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y nginx
    systemctl enable nginx
    systemctl start nginx
  EOF
}