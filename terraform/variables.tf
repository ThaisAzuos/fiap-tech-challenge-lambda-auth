variable "region" {
  default = "us-east-1"
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
