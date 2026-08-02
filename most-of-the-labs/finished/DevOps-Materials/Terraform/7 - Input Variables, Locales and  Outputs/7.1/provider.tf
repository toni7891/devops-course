terraform {
  required_version = "~> 1.7"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 6.0"
    }
  }
}

# AMI ID - eu-west-1: ami-0ec2a5ff1be0688fa
# AMI ID - us-east-1: ami-00de3875b03809ec5
provider "aws" {
  region = var.aws_region
#   region = var.aws_region[0]
}