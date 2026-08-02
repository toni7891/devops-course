variable "instance_type" {
  type        = string
  description = "EC2 instance type."
}

variable "key_name" {
  type        = string
  description = "AWS key pair name."
}

variable "public_key_path" {
  type        = string
  description = "Path to the SSH public key file."
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID for the EC2 instances."
}

variable "security_group_ids" {
  type        = list(string)
  description = "Security group IDs attached to the EC2 instances."
}

variable "app_node_count" {
  type        = number
  description = "Number of app nodes to create."
}

variable "associate_public_ip" {
  type        = bool
  description = "Whether to associate public IP addresses with instances."
}

variable "loki_instance_name" {
  type        = string
  description = "Name tag for the Loki/Grafana instance."
}

variable "app_node_name_prefix" {
  type        = string
  description = "Name tag prefix for app nodes."
}
