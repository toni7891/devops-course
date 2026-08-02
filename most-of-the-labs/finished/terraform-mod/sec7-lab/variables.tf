variable "ec2_instance_type" {
  type        = string
  default     = "t2.micro"
  description = "The type of the managed EC2 instances."
  
  validation {
    condition     = startswith(var.ec2_instance_type, "t3.")
    error_message = "Only supports T3 family."
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