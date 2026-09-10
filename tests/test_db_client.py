import pytest
from unittest.mock import patch, MagicMock, call
from db_client import DBClient


def _cursor_retornando(resultado):
    """Monta connection/cursor mockados em que fetchone devolve `resultado`."""
    cursor = MagicMock()
    cursor.fetchone.return_value = resultado
    conn = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


# --------------------------------------------------------------------------
# __init__
# --------------------------------------------------------------------------

def test_init_usa_argumentos_explicitos():
    client = DBClient(host='db.local', dbname='oficina', user='app', password='s3cr3t')

    assert client.host == 'db.local'
    assert client.dbname == 'oficina'
    assert client.user == 'app'
    assert client.password == 's3cr3t'
    assert client.connection is None


def test_init_cai_para_variaveis_de_ambiente(monkeypatch):
    monkeypatch.setenv('DB_HOST', 'env-host')
    monkeypatch.setenv('DB_NAME', 'env-db')
    monkeypatch.setenv('DB_USER', 'env-user')
    monkeypatch.setenv('DB_PASSWORD', 'env-pass')

    client = DBClient()

    assert client.host == 'env-host'
    assert client.dbname == 'env-db'
    assert client.user == 'env-user'
    assert client.password == 'env-pass'


def test_argumento_explicito_tem_precedencia_sobre_ambiente(monkeypatch):
    monkeypatch.setenv('DB_HOST', 'env-host')

    client = DBClient(host='explicito')

    assert client.host == 'explicito'


def test_init_sem_argumento_nem_ambiente_fica_none(monkeypatch):
    for var in ('DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD'):
        monkeypatch.delenv(var, raising=False)

    client = DBClient()

    assert client.host is None
    assert client.dbname is None
    assert client.user is None
    assert client.password is None


# --------------------------------------------------------------------------
# _get_connection
# --------------------------------------------------------------------------

@patch('db_client.psycopg2.connect')
def test_get_connection_repassa_credenciais(mock_connect):
    client = DBClient(host='db.local', dbname='oficina', user='app', password='s3cr3t')

    client._get_connection()

    mock_connect.assert_called_once_with(
        host='db.local', database='oficina', user='app', password='s3cr3t')


@patch('db_client.psycopg2.connect')
def test_get_connection_reaproveita_conexao_existente(mock_connect):
    client = DBClient(host='db.local')

    primeira = client._get_connection()
    segunda = client._get_connection()

    assert primeira is segunda
    # A conexão é criada uma única vez: a Lambda reusa o container entre invocações.
    mock_connect.assert_called_once()


# --------------------------------------------------------------------------
# check_cpf
# --------------------------------------------------------------------------

@patch('db_client.psycopg2.connect')
def test_check_cpf_retorna_cliente_quando_encontrado(mock_connect):
    conn, cursor = _cursor_retornando(('52998224725', 'Maria Souza'))
    mock_connect.return_value = conn

    resultado = DBClient(host='db.local').check_cpf('52998224725')

    assert resultado == {'id': '52998224725', 'nome': 'Maria Souza'}


@patch('db_client.psycopg2.connect')
def test_check_cpf_usa_query_parametrizada(mock_connect):
    conn, cursor = _cursor_retornando(('52998224725', 'Maria Souza'))
    mock_connect.return_value = conn

    DBClient(host='db.local').check_cpf('52998224725')

    query, parametros = cursor.execute.call_args[0]
    # O CPF vai como parâmetro, nunca interpolado na string — evita SQL injection.
    assert '%s' in query
    assert parametros == ('52998224725',)
    assert '52998224725' not in query


@patch('db_client.psycopg2.connect')
def test_check_cpf_retorna_none_quando_nao_encontrado(mock_connect):
    conn, _ = _cursor_retornando(None)
    mock_connect.return_value = conn

    assert DBClient(host='db.local').check_cpf('00000000000') is None


@patch('db_client.psycopg2.connect')
def test_check_cpf_fecha_o_cursor(mock_connect):
    conn, cursor = _cursor_retornando(('52998224725', 'Maria Souza'))
    mock_connect.return_value = conn

    DBClient(host='db.local').check_cpf('52998224725')

    cursor.close.assert_called_once()


@patch('db_client.psycopg2.connect')
def test_check_cpf_retorna_none_quando_conexao_falha(mock_connect):
    mock_connect.side_effect = Exception('could not connect to server')

    assert DBClient(host='db.local').check_cpf('52998224725') is None


@patch('db_client.psycopg2.connect')
def test_check_cpf_retorna_none_quando_query_falha(mock_connect):
    conn = MagicMock()
    conn.cursor.return_value.execute.side_effect = Exception('relation does not exist')
    mock_connect.return_value = conn

    assert DBClient(host='db.local').check_cpf('52998224725') is None


@patch('db_client.psycopg2.connect')
def test_falha_no_banco_e_registrada(mock_connect, capsys):
    mock_connect.side_effect = Exception('could not connect to server')

    DBClient(host='db.local').check_cpf('52998224725')

    assert 'Database error' in capsys.readouterr().out
