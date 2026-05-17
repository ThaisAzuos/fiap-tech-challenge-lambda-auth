from cpf_validator import validate_cpf
from jwt_generator import generate_jwt
from db_client import DBClient
from logger import logger
import uuid

class AuthService:
    def __init__(self):
        self.db_client = DBClient()

    def authenticate(self, cpf, correlation_id=None):
        """
        Authenticate user by CPF.
        Returns JWT token if valid, None otherwise.
        """
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        logger.log('INFO', f'Starting authentication for CPF: {cpf}', correlation_id, cpf=cpf)

        # Validate CPF format
        if not validate_cpf(cpf):
            logger.log('WARNING', 'Invalid CPF format', correlation_id, cpf=cpf)
            return None

        # Check if customer exists in DB
        customer = self.db_client.check_cpf(cpf)
        if not customer:
            logger.log('WARNING', 'Customer not found for CPF', correlation_id, cpf=cpf)
            return None

        # Generate JWT
        try:
            token = generate_jwt(cpf)
            logger.log('INFO', 'Authentication successful', correlation_id, cpf=cpf, user_id=customer['id'])
            return {
                'token': token,
                'expiry': 3600,
                'user_id': customer['id'],
                'correlation_id': correlation_id
            }
        except Exception as e:
            logger.log('ERROR', f'JWT generation failed: {str(e)}', correlation_id, cpf=cpf)
            return None
