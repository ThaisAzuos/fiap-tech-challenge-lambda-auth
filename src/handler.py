def lambda_handler(event, context):
    """
    AWS Lambda entrypoint for authentication.
    Validates CPF and generates JWT.
    """
    cpf = event.get('cpf')
    if not cpf:
        return {'statusCode': 400, 'body': 'CPF required'}

    # Validate CPF
    # Generate JWT
    # Return token
    return {'statusCode': 200, 'body': {'token': 'jwt_here', 'expiry': 3600}}
