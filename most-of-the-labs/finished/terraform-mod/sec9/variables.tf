variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "subnet_count" {
  type    = number
  default = 2

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

