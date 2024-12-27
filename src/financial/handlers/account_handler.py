from uuid import UUID
from typing import List, Optional, Any, Union
from datetime import datetime
from decimal import Decimal

from src.financial.models import AccountModel
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.database_adapter import DatabaseHandler, Databases
from src.financial.exceptions.handler_errors import account_handler_error


class AccountHandler:
    def __init__(self, database: Union[DatabaseAdapterInterface, DatabaseHandler] = DatabaseHandler(database=Databases.ACCOUNTS)):
        # Valida se o tipo do argumento 'database'
        if not (isinstance(database, (DatabaseAdapterInterface, DatabaseHandler)) or 
                (isinstance(database, type) and issubclass(database, (DatabaseAdapterInterface, DatabaseHandler)))):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'databese'")
        self._database = database
        self._refresh_cache()
    
    @property
    def database(self):
        return self._database
    
    @database.setter
    def database(self, value: Union[DatabaseAdapterInterface, DatabaseHandler]):
        # Valida se o tipo do argumento 'value'
        if not (isinstance(value, (DatabaseAdapterInterface, DatabaseHandler)) or 
                (isinstance(value, type) and issubclass(value, (DatabaseAdapterInterface, DatabaseHandler)))):
            raise account_handler_error.UnexpectedDatabaseTypeError("Tipo inesperado do argumento 'value'")
        self._database = value
    
    def _refresh_cache(self):
        if not hasattr(self, "_cache"):
            self._cache = list()
        self._cache.extend(self._database.get_all())
    
    def _get_cache_by_id(self, id: UUID):
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        return next((account for account in self._cache if account.id == id), None)
    
    def create_account(self, account: AccountModel):
        # Valida se o tipo do argumento 'account'
        if not isinstance(account, AccountModel):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'account'")
        self._database.insert(account)
        self._refresh_cache()
    
    def delete_account(self, id: UUID):
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        self._database.delete(id)
        self._refresh_cache()
    
    def update_account(self, id: UUID, account: AccountModel):
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'account'
        if not isinstance(account, AccountModel):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'account'")
        self._database.update(id, account)
        self._refresh_cache()
    
    def get_account(self, id: UUID) -> Optional[AccountModel]:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        if cached_account:=self._get_cache_by_id(id=id):
            return cached_account
        return self._database.get(id)
    
    def get_all_accounts(self):
        if cache:=self._cache:
            return cache
        return self._database.get_all()
    
    def _change_attribute(self, id: UUID, name: str, value: Any):
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'name'
        if not isinstance(name, str):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'name'")
        
        if cached_account:=self._get_cache_by_id(id=id):
            cached_account.__setattr__(name, value)
            self.update_account(
                id=id,
                account=cached_account
            )
        
        else:
            trasaction = self.get_account(id=id)
            trasaction.__setattr__(name, value)
            self.update_trasaction(
                id=id,
                account=trasaction
            )
    
    def added_balance(self, id: UUID, amount: Decimal) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'id'")
        # Valida se o tipo do argumento 'amount'
        if not isinstance(amount, Decimal):
            raise account_handler_error.UnexpectedArgumentTypeError("Tipo inesperado do argumento 'amount'")
        account = self._get_cache_by_id(id=id) or self.get_account(id=id)
        account.added_balance(amount=amount)
        self.update_account(id=id, account=account)
    
    def subtract_balance(self, id: UUID, amount: Decimal) -> None:
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError()
        # Valida se o tipo do argumento 'amount'
        if not isinstance(amount, Decimal):
            raise account_handler_error.UnexpectedArgumentTypeError()
        account = self._get_cache_by_id(id=id) or self.get_account(id=id)
        account.subtract_balance(amount=amount)
        self.update_account(id=id, account=account)
    
    def change_name(self, id: UUID, name: str):
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError()
        # Valida se o tipo do argumento 'name'
        if not isinstance(name, str):
            raise account_handler_error.UnexpectedArgumentTypeError()
        self._change_attribute(id=id, name="name", value=name)
    
    def change_description(self, id: UUID, description: str):
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError()
        # Valida se o tipo do argumento 'description'
        if not isinstance(description, str):
            raise account_handler_error.UnexpectedArgumentTypeError()
        self._change_attribute(id=id, name="description", value=description)
    
    def change_tag_id(self, id: UUID, tag_id: UUID):
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError()
        # Valida se o tipo do argumento 'tag_id'
        if not isinstance(tag_id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError()
        self._change_attribute(id=id, name="tag_id", value=tag_id)
    
    def change_balance(self, id: UUID, balance: Decimal):
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError()
        # Valida se o tipo do argumento 'balance'
        if not isinstance(balance, Decimal):
            raise account_handler_error.UnexpectedArgumentTypeError()
        self._change_attribute(id=id, name="balance", value=balance)
    
    def change_created_at(self, id: UUID, created_at: datetime):
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError()
        # Valida se o tipo do argumento 'created_at'
        if not isinstance(created_at, datetime):
            raise account_handler_error.UnexpectedArgumentTypeError()
        self._change_attribute(id=id, name="created_at", value=created_at)
    
    def change_user_id(self, id: UUID, user_id: UUID):
        # Valida se o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError()
        # Valida se o tipo do argumento 'user_id'
        if not isinstance(user_id, UUID):
            raise account_handler_error.UnexpectedArgumentTypeError()
        self._change_attribute(id=id, name="user_id", value=user_id)




