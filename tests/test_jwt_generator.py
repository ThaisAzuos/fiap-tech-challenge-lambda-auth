import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from jwt_generator import generate_jwt


@pytest.fixture(autouse=True)
def test_rsa_key(monkeypatch):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    ).decode()
    monkeypatch.setenv('JWT_PRIVATE_KEY', pem)


def test_generate_jwt_returns_token():
    token = generate_jwt('52998224725')
    assert token is not None
    assert isinstance(token, str)
    assert len(token.split('.')) == 3


def test_generate_jwt_different_cpfs():
    token1 = generate_jwt('52998224725')
    token2 = generate_jwt('11144477735')
    assert token1 != token2


def test_generate_jwt_missing_key(monkeypatch):
    monkeypatch.delenv('JWT_PRIVATE_KEY', raising=False)
    with pytest.raises(ValueError):
        generate_jwt('52998224725')
