resource "aws_lambda_function" "auth" {
  function_name = "fiap-tech-challenge-lambda-auth"
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.auth.repository_url}:latest"
  role          = aws_iam_role.lambda_role.arn

  environment {
    variables = {
      VERSION         = "1.0.0"
      DB_HOST         = var.db_host
      DB_NAME         = var.db_name
      DB_USER         = var.db_user
      DB_PASSWORD     = var.db_password
      JWT_PRIVATE_KEY = var.jwt_private_key # Adicionado a chave privada JWT
    }
  }

  layers = [var.newrelic_lambda_layer_arn] # Adicionado o New Relic Lambda Layer

  timeout     = 30
  memory_size = 256

  depends_on = [aws_ecr_repository.auth]
}

resource "aws_ecr_repository" "auth" {
  name = "fiap-tech-challenge-lambda-auth"
}

resource "aws_ecr_lifecycle_policy" "auth" {
  repository = aws_ecr_repository.auth.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 5 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 5
      }
      action = {
        type = "expire"
      }
    }]
  })
}
