from uuid import UUID
from typing import List, Optional, Any, Union
from datetime import datetime

from src.financial.models import AccountTagModel
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.database_adapter import DatabaseHandler, Databases
from src.financial.exceptions.handler_errors import account_tag_handler_error


class AccountTagHandler:
    def __init__(self, database: Union[DatabaseAdapterInterface, DatabaseHandler] = DatabaseHandler(database=Databases.ACCOUNTS_TAGS)):
        # Valida se o tipo do argumento 'database'
        if not (isinstance(database, (DatabaseAdapterInterface, DatabaseHandler)) or 
                (isinstance(database, type) and issubclass(database, (DatabaseAdapterInterface, DatabaseHandler)))):
            raise account_tag_handler_error.UnexpectedDatabaseTypeError("Tipo inesperado do argumento 'databese'")
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
            raise account_tag_handler_error.UnexpectedDatabaseTypeError("Tipo inesperado do argumento 'value'")
        self._database = value
    
    def _refresh_cache(self) -> None:
        if not hasattr(self, "_cache"):
            self._cache = list()
        self._cache.extend(self._database.get_all())
    
    def _get_cache_by_id(self, id: UUID) -> Optional[AccountTagModel]:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        return next((account_tag for account_tag in self._cache if account_tag.id == id), None)
    
    def create_account_tag(self, account_tag: AccountTagModel) -> None:
        # Valida se o tipo do argumento 'account_tag'
        if not isinstance(account_tag, AccountTagModel):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'account_tag'")
        self._database.insert(account_tag)
        self._refresh_cache()
    
    def delete_account_tag(self, id: UUID) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        self._database.delete(id)
        self._refresh_cache()
    
    def update_account_tag(self, id: UUID, account_tag: AccountTagModel) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'account_tag'
        if not isinstance(account_tag, AccountTagModel):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'account_tag'")
        self._database.update(id, account_tag)
        self._refresh_cache()
    
    def get_account_tag(self, id: UUID) -> Optional[AccountTagModel]:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        if cached_account_tag:=self._get_cache_by_id(id=id):
            return cached_account_tag
        return self._database.get(id)
    
    def get_all_account_tags(self) -> List[AccountTagModel]:
        if cache:=self._cache:
            return cache
        return self._database.get_all()
    
    def _change_attribute(self, id: UUID, name: str, value: Any) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'name'
        if not isinstance(name, str):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'name'")
        
        if cached_account_tag:=self._get_cache_by_id(id=id):
            cached_account_tag.__setattr__(name, value)
            self.update_account_tag(
                id=id,
                account_tag=cached_account_tag
            )
        
        else:
            trasaction = self.get_account_tag(id=id)
            trasaction.__setattr__(name, value)
            self.update_trasaction(
                id=id,
                account_tag=trasaction
            )
    
    def change_name(self, id: UUID, name: str) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'name'
        if not isinstance(name, str):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'name'")
        self._change_attribute(id=id, name="name", value=name)
    
    def change_created_at(self, id: UUID, created_at: datetime) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'created_at'
        if not isinstance(created_at, datetime):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'created_at'")
        self._change_attribute(id=id, name="created_at", value=created_at)
    
    def change_user_id(self, id: UUID, user_id: UUID) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'user_id'
        if not isinstance(user_id, UUID):
            raise account_tag_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'user_id'")
        self._change_attribute(id=id, name="user_id", value=user_id)
