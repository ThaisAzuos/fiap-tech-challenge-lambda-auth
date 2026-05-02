import pytest
from src.cpf_validator import validate_cpf

def test_valid_cpf():
    """Test valid CPF"""
    assert validate_cpf('12345678901') == False  # This is actually invalid, but for test
    assert validate_cpf('52998224725') == True   # Valid CPF

def test_invalid_cpf_format():
    """Test invalid CPF formats"""
    assert validate_cpf('') == False
    assert validate_cpf(None) == False
    assert validate_cpf('123') == False  # Too short
    assert validate_cpf('123456789012') == False  # Too long
    assert validate_cpf('11111111111') == False  # All same digits

def test_cpf_with_formatting():
    """Test CPF with dots and dash"""
    assert validate_cpf('529.982.247-25') == True
    assert validate_cpf('52998224725') == True
