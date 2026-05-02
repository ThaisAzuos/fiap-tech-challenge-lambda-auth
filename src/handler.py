import json
from auth_service import AuthService
from logger import logger
import uuid

def lambda_handler(event, context):
    """
    AWS Lambda entrypoint for authentication.
    Validates CPF and generates JWT.
    """
    correlation_id = event.get('correlation_id') or str(uuid.uuid4())

    try:
        logger.log('INFO', 'Lambda invocation started', correlation_id)

        # Parse request body
        if 'body' in event:
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
        else:
            body = event

        cpf = body.get('cpf')
        if not cpf:
            logger.log('WARNING', 'CPF not provided in request', correlation_id)
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'CPF is required',
                    'correlation_id': correlation_id
                })
            }

        # Authenticate
        auth_service = AuthService()
        result = auth_service.authenticate(cpf, correlation_id)

        if result:
            logger.log('INFO', 'Authentication successful', correlation_id, user_id=result['user_id'])
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(result)
            }
        else:
            logger.log('WARNING', 'Authentication failed', correlation_id)
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Invalid CPF or customer not found',
                    'correlation_id': correlation_id
                })
            }

    except Exception as e:
        logger.log('ERROR', f'Unexpected error: {str(e)}', correlation_id)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Internal server error',
                'correlation_id': correlation_id
            })
        }
