import jwt
import time
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from logger import logger # Assumindo que o logger está disponível para registro de erros

def generate_jwt(cpf):
    """
    Generate JWT token with RS256 for authenticated CPF.
    The private key is loaded from the 'JWT_PRIVATE_KEY' environment variable.
    """
    private_key_pem = os.environ.get('JWT_PRIVATE_KEY')
    if not private_key_pem:
        logger.log('ERROR', 'JWT_PRIVATE_KEY environment variable not set.')
        raise ValueError("JWT_PRIVATE_KEY environment variable is required for JWT signing.")

    try:
        # Load private key
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'), # Garante que seja bytes
            password=None,
            backend=default_backend()
        )
    except Exception as e:
        logger.log('ERROR', f'Falha ao carregar a chave privada: {str(e)}')
        raise ValueError(f"JWT_PRIVATE_KEY inválida: {str(e)}")

    payload = {
        'cpf': cpf,
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600,  # Expira em 1 hora
        'iss': 'fiap-tech-challenge-lambda-auth'
    }

    token = jwt.encode(payload, private_key, algorithm='RS256')
    return token
