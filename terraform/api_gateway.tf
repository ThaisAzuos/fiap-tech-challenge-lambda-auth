resource "aws_api_gateway_rest_api" "auth" {
  name        = "fiap-tech-challenge-lambda-auth"
  description = "API Gateway for JWT authentication via CPF validation"
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
  rest_api_id             = aws_api_gateway_rest_api.auth.id
  resource_id             = aws_api_gateway_resource.auth.id
  http_method             = aws_api_gateway_method.auth.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.auth.invoke_arn
}

# CORS
resource "aws_api_gateway_method" "auth_options" {
  rest_api_id   = aws_api_gateway_rest_api.auth.id
  resource_id   = aws_api_gateway_resource.auth.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "auth_options" {
  rest_api_id = aws_api_gateway_rest_api.auth.id
  resource_id = aws_api_gateway_resource.auth.id
  http_method = aws_api_gateway_method.auth_options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "auth_options" {
  rest_api_id = aws_api_gateway_rest_api.auth.id
  resource_id = aws_api_gateway_resource.auth.id
  http_method = aws_api_gateway_method.auth_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "auth_options" {
  rest_api_id = aws_api_gateway_rest_api.auth.id
  resource_id = aws_api_gateway_resource.auth.id
  http_method = aws_api_gateway_method.auth_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

resource "aws_api_gateway_deployment" "auth" {
  depends_on = [
    aws_api_gateway_integration.auth,
    aws_api_gateway_integration.auth_options
  ]
  rest_api_id = aws_api_gateway_rest_api.auth.id
  stage_name  = "prod"
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auth.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.auth.execution_arn}/*/*"
}
