import jwt
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generate_jwt(cpf, private_key_pem=None):
    """
    Generate JWT token with RS256 for authenticated CPF.
    """
    if not private_key_pem:
        # For testing, use a simple secret (should be replaced with proper RS256)
        payload = {
            'cpf': cpf,
            'iat': int(time.time()),
            'exp': int(time.time()) + 3600,  # 1 hour
            'iss': 'fiap-tech-challenge-lambda-auth'
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    # Load private key
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )

    payload = {
        'cpf': cpf,
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600,  # 1 hour
        'iss': 'fiap-tech-challenge-lambda-auth'
    }

    token = jwt.encode(payload, private_key, algorithm='RS256')
    return token
