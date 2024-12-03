from uuid import UUID
from typing import List, Optional

from src.financial.models import UserModel, AccountModel, TransactionModel, TransactionsTypes
from src.financial.database_handler import DatabaseHandler
from src.financial.exceptions.database_handler_error import (
    DatabaseHandlerError,
    UserDatabaseHandlerError,
    AccountDatabaseHandlerError,
    TransactionDatabaseHandlerError,
)


class FinancialHandler:
    def __init__(self) -> None:
        self.db = DatabaseHandler
    
    def add_user(self, user: UserModel) -> None:
        assert isinstance(user, UserModel)
        existing_user = self.db.handler_user.get(user_id=user.user_id)
        if existing_user:
            raise ...
        self.db.handler_user.insert(user=user)
    
    def add_account(self, account: AccountModel) -> None:
        assert isinstance(account, AccountModel)
        existing_account = self.db.handler_account.get(account_id=account.account_id)
        if existing_account:
            raise ...
        self.db.handler_account.insert(account=account)
    
    def add_transaction(self, transaction: TransactionModel) -> None:
        assert isinstance(transaction, TransactionModel)
        existing_transaction = self.db.handler_transaction.get(transaction_id=transaction.transaction_id)
        if existing_transaction:
            raise ...
        self.db.handler_transaction.insert(transaction=transaction)
    
    def update_user(self, user_id: UUID, user: UserModel) -> None:
        existing_user = self.db.handler_user.get(user_id=user.user_id)
        if existing_user:
            self.db.handler_user.update(user_id=user_id, user=user)
        else:
            raise ...
    
    def update_account(self, account_id: UUID, account: AccountModel) -> None:
        existing_account = self.db.handler_account.get(account_id=account_id)
        if existing_account:
            self.db.handler_account.update(account_id=account_id, account=account)
        else:
            raise ...
    
    def update_transaction(self, transaction_id: UUID, transaction: TransactionModel) -> None:
        existing_transaction = self.db.handler_transaction.get(transaction_id=transaction.transaction_id)
        if existing_transaction:
            self.db.handler_transaction.update(transaction_id=transaction_id, transaction=transaction)
        else:
            raise ...
    
    def remove_user(self, user_id: UUID) -> None:
        assert isinstance(user_id, UUID)
        self.db.handler_user.delete(user_id=user_id)
    
    def remove_account(self, account_id: UUID) -> None:
        assert isinstance(account_id, UUID)
        self.db.handler_account.delete(account_id=account_id)
    
    def remove_transaction(self, transaction_id: UUID) -> None:
        assert isinstance(transaction_id, UUID)
        self._undo_execute_transaction(transaction_id=transaction_id)
        self.db.handler_transaction.delete(transaction_id=transaction_id)
    
    def get_user(self, user_id: UUID) -> Optional[UserModel]:
        return self.db.handler_user.get(user_id=user_id)
    
    def get_account(self, account_id: UUID) -> Optional[AccountModel]:
        return self.db.handler_account.get(account_id=account_id)
    
    def get_transaction(self, transaction_id: UUID) -> Optional[TransactionModel]:
        return self.db.handler_transaction.get(transaction_id=transaction_id)
    
    def get_all_users(self) -> List[UserModel]:
        return self.db.handler_user.get_all()
    
    def get_all_accounts(self) -> List[AccountModel]:
        return self.db.handler_account.get_all()
    
    def get_all_transactions(self) -> List[TransactionModel]:
        return self.db.handler_transaction.get_all()
    
    def _execute_transaction(self, transaction_id: UUID) -> None:
        assert isinstance(transaction_id, UUID)
        transaction = self.db.handler_transaction.get(transaction_id=transaction_id)
        if transaction:
            if not transaction.status and transaction.calculate:
                
                self.update_transaction(transaction_id=transaction_id, transaction=transaction)
                
                destination_account = self.db.handler_account.get(transaction.destination)
                origin_account = self.db.handler_account.get(transaction.origin)
                
                match transaction.transaction_type:
                    case TransactionsTypes.DEPOSIT:
                        destination_account.balance += transaction.amount
                        self.update_account(account_id=destination_account.account_id, account=destination_account)
                    case TransactionsTypes.WITHDRAW:
                        destination_account.balance -= transaction.amount
                        self.update_account(account_id=destination_account.account_id, account=destination_account)
                    case TransactionsTypes.TRANSFER:
                        if not origin_account:
                            raise ...
                        origin_account.balance -= transaction.amount
                        destination_account.balance += transaction.amount
                        self.update_account(account_id=origin_account.account_id, account=origin_account)
                        self.update_account(account_id=destination_account.account_id, account=destination_account)
                    case TransactionsTypes.ADJUSTMENT:
                        destination_account.balance += transaction.amount
                        self.update_account(account_id=destination_account.account_id, account=destination_account)
                    case _:
                        raise ...
            else:
                raise ...
        else:
            raise ...
    
    def _undo_execute_transaction(self, transaction_id: UUID) -> None:
        assert isinstance(transaction_id, UUID)
        transaction = self.db.handler_transaction.get(transaction_id=transaction_id)
        if transaction:
            if not transaction.status and transaction.calculate:
                
                self.update_transaction(transaction_id=transaction_id, transaction=transaction)
                
                destination_account = self.db.handler_account.get(transaction.destination)
                origin_account = self.db.handler_account.get(transaction.origin)
                
                match transaction.transaction_type:
                    case TransactionsTypes.DEPOSIT:
                        destination_account.balance -= transaction.amount
                        self.update_account(account_id=destination_account.account_id, account=destination_account)
                    case TransactionsTypes.WITHDRAW:
                        destination_account.balance += transaction.amount
                        self.update_account(account_id=destination_account.account_id, account=destination_account)
                    case TransactionsTypes.TRANSFER:
                        if not origin_account:
                            raise ...
                        origin_account.balance += transaction.amount
                        destination_account.balance -= transaction.amount
                        self.update_account(account_id=origin_account.account_id, account=origin_account)
                        self.update_account(account_id=destination_account.account_id, account=destination_account)
                    case TransactionsTypes.ADJUSTMENT:
                        destination_account.balance -= transaction.amount
                        self.update_account(account_id=destination_account.account_id, account=destination_account)
                    case _:
                        raise ...
            else:
                raise ...
        else:
            raise ...




