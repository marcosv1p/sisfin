from uuid import UUID
from typing import List, Optional, Any, Union
from datetime import datetime

from src.financial.models import UserModel
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.database_adapter import DatabaseHandler, Databases
from src.financial.exceptions.handler_errors import user_handler_error


class UserHandler:
    def __init__(self, database: Union[DatabaseAdapterInterface, DatabaseHandler] = DatabaseHandler(database=Databases.USERS)):
        # Valida se o tipo do argumento 'database'
        if not (isinstance(database, (DatabaseAdapterInterface, DatabaseHandler)) or 
                (isinstance(database, type) and issubclass(database, (DatabaseAdapterInterface, DatabaseHandler)))):
            raise user_handler_error.UnexpectedDatabaseTypeError(error_message="Tipo inesperado do argumento 'databese'")
        self._database = database
        self._refresh_cache()
    
    @property
    def database(self) -> Union[DatabaseAdapterInterface, DatabaseHandler]:
        return self._database
    
    @database.setter
    def database(self, value: Union[DatabaseAdapterInterface, DatabaseHandler]) -> None:
        # Valida se o tipo do argumento 'value'
        if not (isinstance(value, (DatabaseAdapterInterface, DatabaseHandler)) or 
                (isinstance(value, type) and issubclass(value, (DatabaseAdapterInterface, DatabaseHandler)))):
            raise user_handler_error.UnexpectedDatabaseTypeError(error_message="Tipo inesperado do argumento 'value'")
        self._database = value
    
    def _refresh_cache(self) -> None:
        if not hasattr(self, "_cache"):
            self._cache = list()
        self._cache.extend(self._database.get_all())
    
    def _get_cache_by_id(self, id: UUID) -> Optional[UserModel]:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        return next((user for user in self._cache if user.id == id), None)
    
    def create_user(self, user: UserModel) -> None:
        # Valida se o tipo do argumento 'user'
        if not isinstance(user, UserModel):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'user'")
        self._database.insert(user)
        self._refresh_cache()
    
    def delete_user(self, id: UUID) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        self._database.delete(id)
        self._refresh_cache()
    
    def update_user(self, id: UUID, user: UserModel) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'user'
        if not isinstance(user, UserModel):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'user'")
        self._database.update(id, user)
        self._refresh_cache()
    
    def get_user(self, id: UUID) -> Optional[UserModel]:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        if cached_user:=self._get_cache_by_id(id=id):
            return cached_user
        return self._database.get(id)
    
    def get_all_users(self) -> List[UserModel]:
        if cache:=self._cache:
            return cache
        return self._database.get_all()
    
    def _change_attribute(self, id: UUID, name: str, value: Any) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'name'
        if not isinstance(name, str):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'name'")
        
        if cached_user:=self._get_cache_by_id(id=id):
            cached_user.__setattr__(name, value)
            self.update_user(
                id=id,
                user=cached_user
            )
        
        else:
            trasaction = self.get_user(id=id)
            trasaction.__setattr__(name, value)
            self.update_trasaction(
                id=id,
                user=trasaction
            )
    
    def change_nickname(self, id: UUID, nickname: str) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'name'
        if not isinstance(nickname, str):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'nickname'")
        self._change_attribute(id=id, name="nickname", value=nickname)
    
    def change_created_at(self, id: UUID, created_at: datetime) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'created_at'
        if not isinstance(created_at, datetime):
            raise user_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'created_at'")
        self._change_attribute(id=id, name="created_at", value=created_at)
