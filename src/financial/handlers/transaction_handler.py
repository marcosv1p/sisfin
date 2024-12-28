from uuid import UUID
from typing import List, Optional, Any, Union
from datetime import datetime
from decimal import Decimal

from src.financial.models import TransactionModel, TransactionTypes
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.database_adapter import DatabaseHandler, Databases
from src.financial.exceptions.handler_errors import transaction_handler_error


class TransactionHandler:
    def __init__(self, database: Union[DatabaseAdapterInterface, DatabaseHandler] = DatabaseHandler(database=Databases.TRANSACTIONS)):
        # Valida o tipo do argumento 'database'
        if not (isinstance(database, (DatabaseAdapterInterface, DatabaseHandler)) or 
                (isinstance(database, type) and issubclass(database, (DatabaseAdapterInterface, DatabaseHandler)))):
            raise transaction_handler_error.UnexpectedDatabaseTypeError(error_message="Tipo inesperado do argumento 'databese'")
        self._database = database
        self._refresh_cache()
    
    @property
    def database(self) -> Union[DatabaseAdapterInterface, DatabaseHandler]:
        return self._database
    
    @database.setter
    def database(self, value: Union[DatabaseAdapterInterface, DatabaseHandler]) -> None:
        # Valida o tipo do argumento 'value'
        if not (isinstance(value, (DatabaseAdapterInterface, DatabaseHandler)) or 
                (isinstance(value, type) and issubclass(value, (DatabaseAdapterInterface, DatabaseHandler)))):
            raise transaction_handler_error.UnexpectedDatabaseTypeError(error_message="Tipo inesperado do argumento 'value'")
        self._database = value
    
    def _refresh_cache(self) -> None:
        if not hasattr(self, "_cache"):
            self._cache = list()
        self._cache.extend(self._database.get_all())
    
    def _get_cache_by_id(self, id: UUID) -> Optional[TransactionModel]:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        return next((transaction for transaction in self._cache if transaction.id == id), None)
    
    def create_transaction(self, transaction: TransactionModel) -> None:
        # Valida o tipo do argumento 'transaction'
        if not isinstance(transaction, TransactionModel):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'transaction'")
        self._database.insert(transaction)
        self._refresh_cache()
    
    def delete_transaction(self, id: UUID) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        self._database.delete(id)
        self._refresh_cache()
    
    def update_transaction(self, id: UUID, transaction: TransactionModel) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'transaction'
        if not isinstance(transaction, TransactionModel):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'transaction'")
        self._database.update(id, transaction)
        self._refresh_cache()
    
    def get_transaction(self, id: UUID) -> Optional[TransactionModel]:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        if cached_transaction:=self._get_cache_by_id(id=id):
            return cached_transaction
        return self._database.get(id)
    
    def get_all_transactions(self) -> List[TransactionModel]:
        if cache:=self._cache:
            return cache
        return self._database.get_all()
    
    def _change_attribute(self, id: UUID, name: str, value: Any) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'name'
        if not isinstance(name, str):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'name'")
        
        if cached_transaction:=self._get_cache_by_id(id=id):
            cached_transaction.__setattr__(name, value)
            self.update_transaction(
                id=id,
                transaction=cached_transaction
            )
        
        else:
            trasaction = self.get_transaction(id=id)
            trasaction.__setattr__(name, value)
            self.update_trasaction(
                id=id,
                transaction=trasaction
            )
    
    def change_date(self, id: UUID, date: datetime) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'date'
        if not isinstance(date, datetime):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'date'")
        self._change_attribute(id=id, name="date", value=date)
    
    def change_description(self, id: UUID, description: str) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'description'
        if not isinstance(description, str):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'description'")
        self._change_attribute(id=id, name="description", value=description)
    
    def change_amount(self, id: UUID, amount: Decimal) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'amount'
        if not isinstance(amount, Decimal):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'amount'")
        self._change_attribute(id=id, name="amount", value=amount)
    
    def change_transaction_type(self, id: UUID, transaction_type: TransactionTypes) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'transaction_type'
        if not isinstance(transaction_type, TransactionTypes):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'transaction_type'")
        self._change_attribute(id=id, name="transaction_type", value=transaction_type)
    
    def change_paid(self, id: UUID, paid: bool) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'paid'
        if not isinstance(paid, bool):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'paid'")
        self._change_attribute(id=id, name="paid", value=paid)
    
    def change_ignore(self, id: UUID, ignore: bool) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'ignore'
        if not isinstance(ignore, bool):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'ignore'")
        self._change_attribute(id=id, name="ignore", value=ignore)
    
    def change_visible(self, id: UUID, visible: bool) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'visible'
        if not isinstance(visible, bool):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'visible'")
        self._change_attribute(id=id, name="visible", value=visible)
    
    def change_category_id(self, id: UUID, category_id: UUID) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'category_id'
        if not isinstance(category_id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'category_id'")
        self._change_attribute(id=id, name="category_id", value=category_id)
    
    def change_tag_id(self, id: UUID, tag_id: Optional[UUID]) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'tag_id'
        if tag_id is not None and not isinstance(tag_id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'tag_id'")
        self._change_attribute(id=id, name="tag_id", value=tag_id)
    
    def change_account_id_origin(self, id: UUID, account_id_origin: Optional[UUID]) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'account_id_origin'
        if account_id_origin is not None and not isinstance(account_id_origin, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'account_id_origin'")
        self._change_attribute(id=id, name="account_id_origin", value=account_id_origin)
    
    def change_account_id_destination(self, id: UUID, account_id_destination: UUID) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'account_id_destination'
        if not isinstance(account_id_destination, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'account_id_destination'")
        self._change_attribute(id=id, name="account_id_destination", value=account_id_destination)
    
    def change_created_at(self, id: UUID, created_at: datetime) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'created_at'
        if not isinstance(created_at, datetime):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'created_at'")
        self._change_attribute(id=id, name="created_at", value=created_at)
    
    def change_user_id(self, id: UUID, user_id: UUID) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'id'")
        # Valida o tipo do argumento 'user_id'
        if not isinstance(user_id, UUID):
            raise transaction_handler_error.UnexpectedArgumentTypeError(error_message="Tipo inesperado do argumento 'user_id'")
        self._change_attribute(id=id, name="user_id", value=user_id)
