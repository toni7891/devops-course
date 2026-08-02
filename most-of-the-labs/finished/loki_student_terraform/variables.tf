# variables.tf

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "key_name" {
  type    = string
  default = "loki-student-key"
}

variable "ssh_private_key_path" {
  type        = string
  default     = "~/.ssh/loki-student-key"
  description = "Path to the SSH private key used to connect to the instances."
}

variable "ssh_public_key_path" {
  type        = string
  default     = null
  description = "Path to the SSH public key uploaded to AWS. Leave null to use ssh_private_key_path with .pub appended."
}

variable "my_ip_cidr" {
  type        = string
  default     = null
  description = "Your public IP in CIDR format, for example 1.2.3.4/32. Leave null to auto-detect."

  validation {
    condition     = var.my_ip_cidr == null || can(cidrhost(var.my_ip_cidr, 0))
    error_message = "Set my_ip_cidr to your public IP in CIDR format, for example 1.2.3.4/32."
  }
}
