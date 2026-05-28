data "aws_iam_role" "lab_role" {
  name = "LabRole"
}

data "aws_ecr_repository" "auth" {
  name = "fiap-tech-challenge-lambda-auth"
}

resource "aws_lambda_function" "auth" {
  function_name = "fiap-tech-challenge-lambda-auth"
  package_type  = "Image"
  image_uri     = "${data.aws_ecr_repository.auth.repository_url}:latest"
  role          = data.aws_iam_role.lab_role.arn

  environment {
    variables = {
      VERSION         = "1.0.0"
      DB_HOST         = var.db_host
      DB_NAME         = var.db_name
      DB_USER         = var.db_user
      DB_PASSWORD     = var.db_password
      JWT_PRIVATE_KEY = var.jwt_private_key
    }
  }

  layers = var.newrelic_lambda_layer_arn != "" ? [var.newrelic_lambda_layer_arn] : []

  timeout     = 30
  memory_size = 256
}
