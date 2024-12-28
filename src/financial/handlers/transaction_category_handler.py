from uuid import UUID
from typing import List, Optional, Any, Union
from datetime import datetime

from src.financial.models import TransactionCategoryModel
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.database_adapter import DatabaseHandler, Databases
from src.financial.exceptions.handler_errors import transaction_category_handler_error


class TransactionCategoryHandler:
    def __init__(self, database: Union[DatabaseAdapterInterface, DatabaseHandler] = DatabaseHandler(database=Databases.TRANSACTIONS_CATEGORIES)):
        # Valida se o tipo do argumento 'database'
        if not (isinstance(database, (DatabaseAdapterInterface, DatabaseHandler)) or 
                (isinstance(database, type) and issubclass(database, (DatabaseAdapterInterface, DatabaseHandler)))):
            raise transaction_category_handler_error.UnexpectedDatabaseTypeError(error_message="Tipo inesperado do argumento 'databese'")
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
            raise transaction_category_handler_error.UnexpectedDatabaseTypeError(error_message="Tipo inesperado do argumento 'value'")
        self._database = value
    
    def _refresh_cache(self) -> None:
        if not hasattr(self, "_cache"):
            self._cache = list()
        self._cache.extend(self._database.get_all())
    
    def _get_cache_by_id(self, id: UUID) -> Optional[TransactionCategoryModel]:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        return next((transaction_category for transaction_category in self._cache if transaction_category.id == id), None)
    
    def create_transaction_category(self, transaction_category: TransactionCategoryModel) -> None:
        # Valida se o tipo do argumento 'transaction_category'
        if not isinstance(transaction_category, TransactionCategoryModel):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'transaction_category'")
        self._database.insert(transaction_category)
        self._refresh_cache()
    
    def delete_transaction_category(self, id: UUID) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        self._database.delete(id)
        self._refresh_cache()
    
    def update_transaction_category(self, id: UUID, transaction_category: TransactionCategoryModel) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'transaction_category'
        if not isinstance(transaction_category, TransactionCategoryModel):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'transaction_category'")
        self._database.update(id, transaction_category)
        self._refresh_cache()
    
    def get_transaction_category(self, id: UUID) -> Optional[TransactionCategoryModel]:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        if cached_transaction_category:=self._get_cache_by_id(id=id):
            return cached_transaction_category
        return self._database.get(id)
    
    def get_all_transaction_categories(self) -> List[TransactionCategoryModel]:
        if cache:=self._cache:
            return cache
        return self._database.get_all()
    
    def _change_attribute(self, id: UUID, name: str, value: Any) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'name'
        if not isinstance(name, str):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'name'")
        
        if cached_transaction_category:=self._get_cache_by_id(id=id):
            cached_transaction_category.__setattr__(name, value)
            self.update_transaction_category(
                id=id,
                transaction_category=cached_transaction_category
            )
        
        else:
            trasaction = self.get_transaction_category(id=id)
            trasaction.__setattr__(name, value)
            self.update_trasaction(
                id=id,
                transaction_category=trasaction
            )
    
    def change_name(self, id: UUID, name: str) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'name'
        if not isinstance(name, str):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'name'")
        self._change_attribute(id=id, name="name", value=name)
    
    def change_created_at(self, id: UUID, created_at: datetime) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'created_at'
        if not isinstance(created_at, datetime):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'created_at'")
        self._change_attribute(id=id, name="created_at", value=created_at)
    
    def change_user_id(self, id: UUID, user_id: UUID) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'user_id'
        if not isinstance(user_id, UUID):
            raise transaction_category_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'user_id'")
        self._change_attribute(id=id, name="user_id", value=user_id)
