terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = "eu-west-2"
  secret_key = var.AWS_SECRET_ACCESS_KEY
  access_key = var.AWS_ACCESS_KEY_ID
}

## ECR

data "aws_ecr_repository" "lambda-image-repo" {
  name = "c21-george-t3-report"
}

data "aws_ecr_image" "lambda-image-version" {
  repository_name = data.aws_ecr_repository.lambda-image-repo.name
  image_tag       = "latest"
}

## Permissions etc. for the Lambda

# Trust doc (who is allowed to use this)
data "aws_iam_policy_document" "lambda-role-trust-policy-doc" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = [
      "sts:AssumeRole"
    ]
  }
}

# Permissions doc (what are you allowed to do?)
data "aws_iam_policy_document" "lambda-role-permissions-policy-doc" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:eu-west-2:129033205317:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "glue:*",
      "athena:*"
    ]
    resources = ["*"]
  }
}

# Role (thing that can be assumed to get power)
resource "aws_iam_role" "lambda-role" {
  name               = "c21-george-report-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-trust-policy-doc.json
}

# Permissions policy
resource "aws_iam_policy" "lambda-role-permissions-policy" {
  name   = "c21-george-report-permissions-policy"
  policy = data.aws_iam_policy_document.lambda-role-permissions-policy-doc.json
}

# Connect the policy to the role
resource "aws_iam_role_policy_attachment" "lambda-role-policy-connection" {
  role       = aws_iam_role.lambda-role.name
  policy_arn = aws_iam_policy.lambda-role-permissions-policy.arn
}

## Lambda

resource "aws_lambda_function" "report-lambda" {
  function_name = "c21-george-daily-report"
  role          = aws_iam_role.lambda-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.lambda-image-version.image_uri
  timeout       = 300
  memory_size   = 512
}