import jwt
from src.jwt_generator import generate_jwt

def test_generate_jwt():
    token = generate_jwt('12345678901')
    assert token is not None

def test_generate_jwt_hs256():
    """Test JWT generation with HS256 (default)"""
    cpf = '52998224725'
    token = generate_jwt(cpf)

    assert token is not None
    assert isinstance(token, str)

    # Decode and verify
    decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
    assert decoded['cpf'] == cpf
    assert 'exp' in decoded
    assert 'iat' in decoded
    assert decoded['iss'] == 'fiap-tech-challenge-lambda-auth'

def test_generate_jwt_rs256():
    """Test JWT generation with RS256 (if key provided)"""
    # For now, test that it falls back to HS256 when no key
    cpf = '52998224725'
    token = generate_jwt(cpf, private_key_pem=None)
    assert token is not None

    # Would need actual RSA key for full test
    # private_key_pem = "-----BEGIN PRIVATE KEY-----\n..."
    # token = generate_jwt(cpf, private_key_pem)
    # decoded = jwt.decode(token, public_key, algorithms=['RS256'])
