variable "AWS_REGION" {
  description = "Which AWS region to create resources in"
  type        = string
}

variable "AWS_ID" {
  description = "Your AWS access key ID"
  type        = string
  sensitive   = true
}

variable "AWS_SECRET" {
  description = "Your AWS secret access key"
  type        = string
  sensitive   = true
}