variable "subnet_count" {
  type    = number
  default = 3
}

variable "ec2_instance_count" {
  type    = number
  default = 1
}

variable "ec2_instance_config_list" {
  type = list(object({
    instance_type = string
    ami           = string
  }))

  default = []
}