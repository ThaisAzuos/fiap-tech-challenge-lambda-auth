import pytest
import json
from unittest.mock import patch, MagicMock
from src.handler import lambda_handler

@patch('src.auth_service.DBClient')
def test_lambda_handler_success(mock_db_client):
    """Test successful authentication"""
    # Mock DB client
    mock_instance = MagicMock()
    mock_instance.check_cpf.return_value = {'id': 1, 'nome': 'Test User'}
    mock_db_client.return_value = mock_instance

    event = {'cpf': '52998224725'}
    response = lambda_handler(event, None)

    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'token' in body
    assert body['expiry'] == 3600
    assert body['user_id'] == 1
    assert 'correlation_id' in body

@patch('src.auth_service.DBClient')
def test_lambda_handler_invalid_cpf(mock_db_client):
    """Test invalid CPF"""
    event = {'cpf': '11111111111'}  # Invalid CPF
    response = lambda_handler(event, None)

    assert response['statusCode'] == 401
    body = json.loads(response['body'])
    assert 'error' in body

@patch('src.auth_service.DBClient')
def test_lambda_handler_missing_cpf(mock_db_client):
    """Test missing CPF"""
    event = {}
    response = lambda_handler(event, None)

    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert 'error' in body

@patch('src.auth_service.DBClient')
def test_lambda_handler_customer_not_found(mock_db_client):
    """Test customer not found in DB"""
    mock_instance = MagicMock()
    mock_instance.check_cpf.return_value = None
    mock_db_client.return_value = mock_instance

    event = {'cpf': '52998224725'}
    response = lambda_handler(event, None)

    assert response['statusCode'] == 401
    body = json.loads(response['body'])
    assert 'error' in body

def test_lambda_handler_with_body():
    """Test with API Gateway body format"""
    event = {
        'body': json.dumps({'cpf': '52998224725'})
    }

    with patch('src.auth_service.DBClient') as mock_db:
        mock_instance = MagicMock()
        mock_instance.check_cpf.return_value = {'id': 1, 'nome': 'Test'}
        mock_db.return_value = mock_instance

        response = lambda_handler(event, None)
        assert response['statusCode'] == 200
