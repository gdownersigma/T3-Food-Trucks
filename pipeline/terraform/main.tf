terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = var.AWS_REGION
  access_key = var.AWS_ID
  secret_key = var.AWS_SECRET
}

resource "aws_s3_bucket" "data_lake" {
  bucket = "c21-george-food-truck"  
}