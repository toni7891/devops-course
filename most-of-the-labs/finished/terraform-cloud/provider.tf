terraform {
  cloud {
    organization = "TonyVerin"

    workspaces {
      name = "test-worksapce"
    }
  }

  required_providers {
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "random_id" "this" {
  byte_length = 4
}

output "random_id" {
  value = random_id.this.hex
}

