variable "ec2_instance_type" {
  type        = string
  description = "The type of the managed EC2 instances."

  # validation {
  #   condition     = var.ec2_instance_type == "t2.micro" || var.ec2_instance_type == "t3.micro"
  #   error_message = "Only t2.micro and t3.micro instances are supported."
  # }

  validation {
    condition     = contains(["t2.micro", "t3.micro"], var.ec2_instance_type)
    error_message = "Only t2.micro and t3.micro instances are supported."
  }

}

variable "ec2_volume_config" {
  type = object({
    size = number
    type = string
  })
  description = "The size and type of the root block volume for EC2 instances."
  default = {
    size = 10
    type = "gp3"
  }
}

variable "additional_tags" {
  type    = map(string)
  default = {}
}