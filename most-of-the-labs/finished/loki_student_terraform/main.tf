# main.tf

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
    http = {
      source  = "hashicorp/http"
      version = "~> 3.4"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "http" "my_ip" {
  url = "https://ifconfig.me/ip"
}

locals {
  my_ip_cidr       = coalesce(var.my_ip_cidr, "${chomp(data.http.my_ip.response_body)}/32")
  private_key_path = pathexpand(var.ssh_private_key_path)
  public_key_path  = pathexpand(coalesce(var.ssh_public_key_path, "${var.ssh_private_key_path}.pub"))
}

module "network" {
  source = "./modules/network"
}

module "security_group" {
  source = "./modules/security-group"

  name       = "loki-student-sg"
  vpc_id     = module.network.vpc_id
  my_ip_cidr = local.my_ip_cidr
}

module "compute" {
  source = "./modules/compute"

  instance_type        = var.instance_type
  key_name             = var.key_name
  public_key_path      = local.public_key_path
  subnet_id            = module.network.subnet_id
  security_group_ids   = [module.security_group.security_group_id]
  app_node_count       = 2
  associate_public_ip  = true
  loki_instance_name   = "loki-student-server"
  app_node_name_prefix = "loki-student-node"
}

module "ssh_commands" {
  source = "./modules/ssh-commands"

  instances        = module.compute.instances
  private_key_path = local.private_key_path
  output_path      = "${path.module}/ssh_commands.txt"
}

output "ssh_commands_file" {
  description = "Path to the generated SSH commands file."
  value       = module.ssh_commands.file_path
}

output "ssh_commands" {
  description = "SSH commands for connecting to each instance."
  value       = module.ssh_commands.commands
}

output "instance_ips" {
  description = "Public and private IP addresses for the tutorial."
  value       = module.compute.instances
}
