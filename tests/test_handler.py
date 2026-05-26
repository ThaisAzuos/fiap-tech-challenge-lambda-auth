import pytest
import json
from unittest.mock import patch, MagicMock
from handler import lambda_handler


@patch('auth_service.generate_jwt')
@patch('auth_service.DBClient')
def test_lambda_handler_success(mock_db_client, mock_generate_jwt):
    mock_generate_jwt.return_value = 'fake.jwt.token'
    mock_instance = MagicMock()
    mock_instance.check_cpf.return_value = {'id': '52998224725', 'nome': 'Test User'}
    mock_db_client.return_value = mock_instance

    event = {'body': {'cpf': '52998224725'}}
    response = lambda_handler(event, None)

    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'token' in body
    assert body['expiry'] == 3600
    assert 'user_id' in body
    assert 'correlation_id' in body


@patch('auth_service.DBClient')
def test_lambda_handler_invalid_cpf(mock_db_client):
    event = {'body': {'cpf': '11111111111'}}
    response = lambda_handler(event, None)

    assert response['statusCode'] == 401
    body = json.loads(response['body'])
    assert 'error' in body


@patch('auth_service.DBClient')
def test_lambda_handler_missing_cpf(mock_db_client):
    event = {'body': {}}
    response = lambda_handler(event, None)

    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert 'error' in body


@patch('auth_service.generate_jwt')
@patch('auth_service.DBClient')
def test_lambda_handler_customer_not_found(mock_db_client, mock_generate_jwt):
    mock_instance = MagicMock()
    mock_instance.check_cpf.return_value = None
    mock_db_client.return_value = mock_instance

    event = {'body': {'cpf': '52998224725'}}
    response = lambda_handler(event, None)

    assert response['statusCode'] == 401
    body = json.loads(response['body'])
    assert 'error' in body


@patch('auth_service.generate_jwt')
@patch('auth_service.DBClient')
def test_lambda_handler_with_body_string(mock_db_client, mock_generate_jwt):
    mock_generate_jwt.return_value = 'fake.jwt.token'
    mock_instance = MagicMock()
    mock_instance.check_cpf.return_value = {'id': '52998224725', 'nome': 'Test'}
    mock_db_client.return_value = mock_instance

    event = {'body': json.dumps({'cpf': '52998224725'})}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
