import re
from rich.console import Console
from rich.traceback import install
from src.exceptions.user_errors.password_errors import (
    PasswordLengthError, 
    PasswordUppercaseError, 
    PasswordLowercaseError, 
    PasswordDigitError, 
    PasswordSpecialCharError
)

install(show_locals=True, max_frames=1, extra_lines=3)

console = Console(width=500)

def validate_password(password: str) -> None:
    exceptions = []
    if len(password) < 8:
        exceptions.append(PasswordLengthError())
    if not re.search(r"[A-Z]", password):
        exceptions.append(PasswordUppercaseError())
    if not re.search(r"[a-z]", password):
        exceptions.append(PasswordLowercaseError())
    if not re.search(r"\d", password):
        exceptions.append(PasswordDigitError())
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        exceptions.append(PasswordSpecialCharError())
    
    if exceptions:
        raise ExceptionGroup("Erros de Validação de Senha", exceptions)