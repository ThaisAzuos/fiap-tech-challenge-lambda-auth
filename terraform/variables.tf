variable "region" {
  default = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "environment" {
  default = "dev"
}

variable "db_host" {
  description = "RDS PostgreSQL host"
  type        = string
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "oficina"
}

variable "db_user" {
  description = "Database username"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "jwt_private_key" {
  description = "Private key for JWT signing (RS256)"
  type        = string
  sensitive   = true
}

variable "newrelic_lambda_layer_arn" {
  description = "ARN of the New Relic Lambda Layer for Python (optional)"
  type        = string
  default     = ""
}
