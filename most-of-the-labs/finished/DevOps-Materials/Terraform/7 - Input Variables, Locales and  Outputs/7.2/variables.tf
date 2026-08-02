variable "ec2_instance_type" {
  type        = string
  default     = "t2.micro"
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

variable "ec2_volume_type" {
  type        = string
  default     = "gp3"
  description = "The volume type of the root block volume attached to EC2 instances. Supported values: gp2 and gp3."
}

variable "ec2_volume_size" {
  type        = number
  default     = 10
  description = "The size in gigabytes of the root block volume attached to EC2 instances."
}