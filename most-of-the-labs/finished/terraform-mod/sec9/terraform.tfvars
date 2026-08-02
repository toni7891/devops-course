subnet_count = 3

ec2_instance_count = 0

ec2_instance_config_list = [
  {
    instance_type = "t3.micro"
    ami           = "ubuntu"
  },
  {
    instance_type = "t3.micro"
    ami           = "nginx"
  }
]
