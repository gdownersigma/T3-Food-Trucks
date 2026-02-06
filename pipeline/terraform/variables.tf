variable "AWS_REGION" {
  type = string
}

variable "AWS_ACCESS_KEY_ID" {
  type      = string
  sensitive = true
}

variable "AWS_SECRET_ACCESS_KEY" {
  type      = string
  sensitive = true
}

variable "ECR_IMAGE_URI" {
  type = string
}

variable "DB_HOST" {
  type = string
}

variable "DB_PORT" {
  type = string
}

variable "DB_NAME" {
  type = string
}

variable "DB_USER" {
  type = string
}

variable "DB_PASSWORD" {
  type      = string
  sensitive = true
}

variable "AWS_ACCOUNT_ID" {
  type = string
}

variable "SUBNET_IDS" {
  type = list(string)
}

variable "SECURITY_GROUP_IDS" {
  type = list(string)
}