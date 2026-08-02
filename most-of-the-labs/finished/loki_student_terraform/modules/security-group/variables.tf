variable "name" {
  type        = string
  description = "Security group name."
}

variable "vpc_id" {
  type        = string
  description = "VPC ID where the security group will be created."
}

variable "my_ip_cidr" {
  type        = string
  description = "Public IP CIDR allowed to access demo services."
}
