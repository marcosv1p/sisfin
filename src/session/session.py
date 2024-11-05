import logging
from pydantic import BaseModel, PrivateAttr, constr
from cryptography.fernet import Fernet
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Dict, Any
from src.user import User
import time
from functools import wraps

# Configuração de logging robusta
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Session(BaseModel):
    __user: User | None = PrivateAttr(default=None)
    __session_id: UUID = PrivateAttr(default_factory=uuid4)
    __created_at: datetime = PrivateAttr(default_factory=datetime.now)
    __start_time: float = PrivateAttr(default_factory=time.monotonic)
    __timeout: int = PrivateAttr(default=0)
    
    def set_user(self, user: User):
        if self.__user is None and not isinstance(self.__user, User):
            self.__user = user
            self.__timeout += 300
            
        else:
            raise ValueError("Usuário já definido na sessão!")
    
    def get_session_data(self) -> dict:
        return {"session_id": self.__session_id, "created_at": self.__created_at}
    
    def is_active(self) -> bool:
        if self.__start_time - time.monotonic() > self.__timeout:
            return False
        else:
            return True


class SessionManager(BaseModel):
    def create_session(self, user: User):
        self.__session = Session()
        self.__session.set_user(user=user)

    