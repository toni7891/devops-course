terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.37.0"
    }
  }
}

# Managed by us, we are creating it.
# resource "aws_s3_bucket" "my_bucket" {
#   bucket = "my-sample-bucket"
# }

# data "aws_s3_bucket" "my_bucket2" {
#   vpc = "not-managed-by-us" #! Will cause an error because the bucket does not exist and we are trying to access it.
# }

# Managed by someone else, we are just reading it, not creating it.
data "aws_s3_bucket" "external_bucket" {
  bucket = "not-managed-by-us"
}

# Data source to read the bucket name from the external bucket.
variable "bucket_name" {
  type        = string
  description = "Variable used to set bucket name"
  default     = "my-default-bucket-name"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name
}

# terraform output

output "bucket_id" {
  value = aws_s3_bucket.my_bucket.id
}

# this is a local variable, it is not stored in the state file and cannot be accessed outside of this configuration.
locals {
  local_example = "This is a local variable"
}

output "local_value" {
  value = local.local_example
}

# Moduels are reusable configurations that can be called multiple times with different parameters. They are defined in separate directories and can be sourced from local paths, Git repositories, or the Terraform Registry.
module "my_module" {
  source = "./module-example"
}