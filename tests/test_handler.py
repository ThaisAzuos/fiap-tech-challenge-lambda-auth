import pytest
from src.handler import lambda_handler

def test_lambda_handler():
    event = {'cpf': '12345678901'}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
