resource "aws_instance" "web" {
  # AMI ID NGINX = "ami-0e15d9a1fb194a3f4"
  # AMI ID UBUNTU = "ami-0e95f7a6cbfd428cb"
  ami                         = "ami-0e15d9a1fb194a3f4" # Bitnami Nginx AMI
  associate_public_ip_address = true
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids = [
    aws_security_group.public_http_traffic.id
  ]


  root_block_device {
    delete_on_termination = true
    volume_size           = 10
    volume_type           = "gp3"
  }

  tags = merge(
    local.common_tags,
    {
      "Name" = "06-resources-web-server"
    }
  )
  lifecycle {
    create_before_destroy = true # Create instance before destroy it, otherwise you will get an error. Defaults: false (only create when `force_destroy` is set) -> https:
  }
}

resource "aws_security_group" "public_http_traffic" {
  name        = "public HTTP traffic"
  description = "Security group allowing traffic on ports 80, 443"
  vpc_id      = aws_vpc.main.id
}

# id: b7e3d1
resource "aws_vpc_security_group_ingress_rule" "http" {
  security_group_id = aws_security_group.public_http_traffic.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"
}

# id: c4k8p9
resource "aws_vpc_security_group_ingress_rule" "https" {
  security_group_id = aws_security_group.public_http_traffic.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
}