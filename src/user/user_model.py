import logging
import re
from pydantic import BaseModel, PrivateAttr, constr
from cryptography.fernet import Fernet
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Dict, Any
from src.exceptions.user_errors.generic_user_error import GenericUserError
from src.user.validate_password import validate_password

# Configuração de logging robusta
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class User(BaseModel):
    name: constr(min_length=3, max_length=67, pattern=re.compile(r"^[a-zA-Z]+$"))
    __password: str = PrivateAttr(default_factory=lambda: str(uuid4()))
    __cryptography_key: bytes = PrivateAttr(default_factory=lambda: Fernet.generate_key())
    __user_id: UUID = PrivateAttr(default_factory=uuid4)
    __created_at: datetime = PrivateAttr(default_factory=datetime.now)
    __changes: List[Dict[str, Any]] = PrivateAttr(default_factory=list)
    
    def metadata(self):
        return {"user_id": self.__user_id, "created_at": self.__created_at, "changes": self.__changes}

    def set_password(self, password: str) -> None:
        """Encrypts the password after validation and stores it."""
        try:
            validate_password(password)
        except GenericUserError as e:
            logging.error(f"Error Code: {e.code.value}, Message: {e.message}")
            raise  # Re-raise após o logging
        
        fernet = Fernet(self.__cryptography_key)
        encrypted_password = fernet.encrypt(password.encode())
        self.__password = encrypted_password
        self.__log_change('password', 'updated')

    def check_password(self, password: str) -> bool:
        """Verifies if the provided password matches the encrypted one."""
        fernet = Fernet(self.__cryptography_key)
        try:
            decrypted_password = fernet.decrypt(self.__password).decode()
            return decrypted_password == password
        except Exception:
            return False

    def __log_change(self, field: str, action: str) -> None:
        """Logs changes made to the User fields."""
        self.__changes.append({
            'field': field,
            'action': action,
            'timestamp': datetime.now()
        })
        logging.info(f"Change logged: {field} - {action}")
