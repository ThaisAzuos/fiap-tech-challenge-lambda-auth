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

variable "jwt_private_key" {
  description = "Private key for JWT signing (RS256)"
  type        = string
  sensitive   = true
}

variable "newrelic_lambda_layer_arn" {
  description = "ARN of the New Relic Lambda Layer for Python"
  type        = string
  # Exemplo de default para us-east-1 e Python 3.9 (verificar a versão correta no New Relic)
  # default     = "arn:aws:lambda:us-east-1:451483290750:layer:NewRelicPython39:XX"
  # O valor exato do ARN deve ser obtido da documentação do New Relic para a região e runtime corretos.
}
