variable "ami_nginx" {
  description = "Amazon Linux 2023 AMI for eu-west-1, nginx installed via user_data (Bitnami's nginx Marketplace AMI was discontinued)"
  type        = string
  default     = "ami-07c0513c442749688"
}

variable "ami_ubuntu" {
  description = "Canonical Ubuntu 24.04 LTS AMI for eu-west-1"
  type        = string
  default     = "ami-04df7d76c1b804451"
}

resource "aws_instance" "web" {
  ami                         = var.ami_nginx
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public.id
  associate_public_ip_address = true

  user_data = <<-EOF
    #!/bin/bash
    dnf install -y nginx
    systemctl enable --now nginx
  EOF

  root_block_device {
    delete_on_termination = true
    volume_size           = 10
    volume_type           = "gp3"
  }

  vpc_security_group_ids = [
    aws_security_group.public_http_traffic.id
  ]

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [tags]
  }

  tags = {
    Name = "06_resources_ec2"
  }
}

resource "aws_security_group" "public_http_traffic" {
  name        = "public HTTP traffic"
  description = "Allow 80 and 443 ports"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "06_resources_sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "http" {
  security_group_id = aws_security_group.public_http_traffic.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "https" {
  security_group_id = aws_security_group.public_http_traffic.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "all_outbound" {
  security_group_id = aws_security_group.public_http_traffic.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

