
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
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}


resource "aws_glue_catalog_database" "c21-george-food_truck_db" {
  name = var.GLUE_DATABASE_NAME
}

resource "aws_iam_role" "glue_crawler_role" {
  name = "c21-george-glue-crawler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "glue_crawler_policy" {
  name = "c21-george-glue-crawler-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${var.S3_BUCKET_NAME}",
          "arn:aws:s3:::${var.S3_BUCKET_NAME}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "glue:*"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_crawler_attachment" {
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = aws_iam_policy.glue_crawler_policy.arn
}

resource "aws_glue_crawler" "food_truck_crawler" {
  name          = "c21-george-food-truck-crawler"
  database_name = aws_glue_catalog_database.c21-george-food_truck_db.name
  role          = aws_iam_role.glue_crawler_role.arn

  s3_target {
    path = "s3://${var.S3_BUCKET_NAME}/input"
  }
}
