from src.cpf_validator import validate_cpf

def test_validate_cpf():
    assert validate_cpf('12345678901') == True
