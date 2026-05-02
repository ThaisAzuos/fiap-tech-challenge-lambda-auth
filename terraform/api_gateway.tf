resource "aws_api_gateway_rest_api" "auth" {
  name = "oficina-auth-api"
}

resource "aws_api_gateway_resource" "auth" {
  rest_api_id = aws_api_gateway_rest_api.auth.id
  parent_id   = aws_api_gateway_rest_api.auth.root_resource_id
  path_part   = "authenticate"
}

resource "aws_api_gateway_method" "auth" {
  rest_api_id   = aws_api_gateway_rest_api.auth.id
  resource_id   = aws_api_gateway_resource.auth.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "auth" {
  rest_api_id = aws_api_gateway_rest_api.auth.id
  resource_id = aws_api_gateway_resource.auth.id
  http_method = aws_api_gateway_method.auth.http_method
  type        = "AWS_PROXY"
  integration_http_method = "POST"
  uri         = aws_lambda_function.auth.invoke_arn
}

resource "aws_api_gateway_deployment" "auth" {
  depends_on = [aws_api_gateway_integration.auth]
  rest_api_id = aws_api_gateway_rest_api.auth.id
  stage_name  = "prod"
}
