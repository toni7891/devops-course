ec2_instance_type = "t3.large"

ec2_volume_config = {
  size = 50
  type = "gp3"
}

additional_tags = {
  ValuesFrom = "prod.terraform.tfvars"
}