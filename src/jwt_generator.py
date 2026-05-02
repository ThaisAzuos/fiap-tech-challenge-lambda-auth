import jwt

def generate_jwt(cpf):
    """
    Generate JWT token for authenticated CPF.
    """
    payload = {'cpf': cpf, 'exp': 3600}
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token
