resource "aws_instance" "web" {
  ami                    = "ami-0ec2a5ff1be0688fa"  # Ubuntu 22.04 AMD64 in eu-west-1
  associate_public_ip_address = true
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public.id

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
}