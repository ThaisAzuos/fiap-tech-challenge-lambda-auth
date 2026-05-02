from src.jwt_generator import generate_jwt

def test_generate_jwt():
    token = generate_jwt('12345678901')
    assert token is not None
