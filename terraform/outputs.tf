output "lambda_arn" {
  value = aws_lambda_function.auth.arn
}

output "api_gateway_url" {
  value = aws_api_gateway_stage.auth.invoke_url
}
