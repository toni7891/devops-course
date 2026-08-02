terraform {
  required_version = "~> 1.14.8"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.39"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
  default_tags {
    tags = {
      "ManagedBy"  = "Terraform"
      "Project"    = "06-resources"
      "CostCenter" = "1234"
    }
  }
}