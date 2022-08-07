terraform {
  required_version = "~> 1.2"

  required_providers {
    aws = {
      version = "~> 4.22.0"
      source  = "hashicorp/aws"
    }
  }
}

# AWS provider
provider "aws" {
  region = "us-west-2"
  default_tags {
    tags = {
      Owner = "YourMom"
    }
  }
}
