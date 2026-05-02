resource "aws_lambda_function" "auth" {
  function_name = "oficina-lambda-auth"
  runtime       = "python3.11"
  handler       = "handler.lambda_handler"
  filename      = "lambda.zip"
  role          = aws_iam_role.lambda_role.arn
}
