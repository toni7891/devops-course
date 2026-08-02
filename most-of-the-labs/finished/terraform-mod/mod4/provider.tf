terraform {
  required_version = ">= 1.7.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = {
      "managed_by"  = "Terraform"
      "project"     = "06-resources"
      "cost_center" = "1234"
    }
  }
}
