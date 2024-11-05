import pytest
from src.exceptions.user_errors.password_errors import (
    PasswordLengthError,
    PasswordUppercaseError,
    PasswordLowercaseError,
    PasswordDigitError,
    PasswordSpecialCharError,
)
from src.user.user_model import User
from src.user.validate_password import validate_password


# Testes para validate_password
def test_valid_password():
    """Testa se a senha válida não gera exceções."""
    try:
        validate_password("Valid1Password!")
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


def test_password_too_short():
    """Testa se uma senha muito curta gera o erro apropriado."""
    with pytest.raises(ExceptionGroup) as exc_info:
        validate_password("Short1!")
    
    assert any(isinstance(exc, PasswordLengthError) for exc in exc_info.value.exceptions)


def test_missing_uppercase():
    """Testa se a falta de letra maiúscula gera o erro apropriado."""
    with pytest.raises(ExceptionGroup) as exc_info:
        validate_password("missinguppercase1!")
    
    assert any(isinstance(exc, PasswordUppercaseError) for exc in exc_info.value.exceptions)


def test_missing_lowercase():
    """Testa se a falta de letra minúscula gera o erro apropriado."""
    with pytest.raises(ExceptionGroup) as exc_info:
        validate_password("MISSINGLOWERCASE1!")
    
    assert any(isinstance(exc, PasswordLowercaseError) for exc in exc_info.value.exceptions)


def test_missing_digit():
    """Testa se a falta de número gera o erro apropriado."""
    with pytest.raises(ExceptionGroup) as exc_info:
        validate_password("MissingDigit!")
    
    assert any(isinstance(exc, PasswordDigitError) for exc in exc_info.value.exceptions)


def test_missing_special_character():
    """Testa se a falta de caractere especial gera o erro apropriado."""
    with pytest.raises(ExceptionGroup) as exc_info:
        validate_password("MissingSpecialChar1")
    
    assert any(isinstance(exc, PasswordSpecialCharError) for exc in exc_info.value.exceptions)


def test_user_password_encryption():
    """Testa se a senha é criptografada corretamente após validação."""
    user = User(name="TestUser")
    password = "Valid1Password!"

    user.set_password(password)
    
    assert user.check_password(password) is True
    assert user.check_password("WrongPassword!") is False


def test_user_invalid_password():
    """Testa se a tentativa de definir uma senha inválida gera erro apropriado."""
    user = User(name="TestUser")
    
    with pytest.raises(ExceptionGroup) as exc_info:
        user.set_password("short")
    
    assert any(isinstance(exc, PasswordLengthError) for exc in exc_info.value.exceptions)
    
    with pytest.raises(ExceptionGroup) as exc_info:
        user.set_password("missinguppercase1")
    
    assert any(isinstance(exc, PasswordUppercaseError) for exc in exc_info.value.exceptions)

    with pytest.raises(ExceptionGroup) as exc_info:
        user.set_password("MISSINGLOWERCASE1!")
    
    assert any(isinstance(exc, PasswordLowercaseError) for exc in exc_info.value.exceptions)

    with pytest.raises(ExceptionGroup) as exc_info:
        user.set_password("MissingDigit!")
    
    assert any(isinstance(exc, PasswordDigitError) for exc in exc_info.value.exceptions)

    with pytest.raises(ExceptionGroup) as exc_info:
        user.set_password("MissingSpecialChar1")
    
    assert any(isinstance(exc, PasswordSpecialCharError) for exc in exc_info.value.exceptions)

