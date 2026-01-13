variable "AWS_REGION" {
  description = "AWS region"
  type        = string
}

variable "AWS_ACCESS_KEY_ID" {
  description = "AWS access key"
  type        = string
  sensitive   = true
}

variable "AWS_SECRET_ACCESS_KEY" {
  description = "AWS secret key"
  type        = string
  sensitive   = true
}

variable "S3_BUCKET_NAME" {
  description = "Name of the S3 bucket to crawl"
  type        = string
}

variable "GLUE_DATABASE_NAME" {
  description = "Name for the Glue database"
  type        = string
}