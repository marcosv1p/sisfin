from enum import Enum

from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.database_adapter import (
    AccountDatabaseAdapter,
    AccountTagDatabaseAdapter,
    TransactionDatabaseAdapter,
    TransactionTagDatabaseAdapter,
    TransactionCategoryDatabaseAdapter,
    UserDatabaseAdapter
)


class Databases(Enum):
    USERS = "user"
    ACCOUNTS = "account"
    ACCOUNTS_TAGS = "account_tag"
    TRANSACTIONS = "transaction"
    TRANSACTIONS_TAGS = "transaction_tag"
    TRANSACTIONS_CATEGORIES = "transaction_category"


class DatabaseHandler:
    def __init__(self, database: Databases) -> DatabaseAdapterInterface:
        assert isinstance(database, Databases)
        match database:
            case Databases.ACCOUNTS:
                _database_match = AccountDatabaseAdapter
            case Databases.ACCOUNTS_TAGS:
                _database_match = AccountTagDatabaseAdapter
            case Databases.TRANSACTIONS:
                _database_match = TransactionDatabaseAdapter
            case Databases.TRANSACTIONS_TAGS:
                _database_match = TransactionTagDatabaseAdapter
            case Databases.TRANSACTIONS_CATEGORIES:
                _database_match = TransactionCategoryDatabaseAdapter
            case Databases.USERS:
                _database_match = UserDatabaseAdapter
            case _:
                _database_match = DatabaseAdapterInterface
        
        # Evitar que o atributo `_database` seja tratado por `__setattr__`
        super().__setattr__('_database', _database_match)
    
    def __getattr__(self, name):
        # Delega chamadas de atributos/métodos inexistentes ao `_database`
        return getattr(self._database, name)
    
    def __setattr__(self, name, value):
        # Delega definições para o _database se já existir nele
        if hasattr(self._database, name):
            setattr(self._database, name, value)
        else:
            super().__setattr__(name, value)
