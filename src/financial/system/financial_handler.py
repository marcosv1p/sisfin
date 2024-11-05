from uuid import UUID
from copy import deepcopy
from typing import List, Any, Optional, Iterable

from src.financial.bank import BankModel
from src.financial.account import AccountModel
from src.financial.transaction import TransactionModel
from src.financial.database_handler import DatabaseHandler
from src.financial.exceptions.financial_handler_error import (
    BankNotFoundError,
    BankAccountNotFoundError,
    TransactionNotFoundError,
    BankAlreadyExistsError,
    BankAccountAlreadyExistsError,
    TransactionAlreadyExistsError,
)


class FinancialHandler:
    def __init__(self) -> None:
        self.load_all_data()
    
    def load_all_data(self) -> None:
        self._load_banks()
        self._load_accounts()
        self._load_transactions()
    
    def _load_banks(self) -> List[BankModel]:
        if not hasattr(self, '_banks'):
            self._banks = DatabaseHandler.db_bank.get_all()
        return self._banks
    
    def _load_accounts(self) -> List[AccountModel]:
        if not hasattr(self, '_accounts'):
            self._load_banks()
            self._accounts = DatabaseHandler.db_account.get_all()
        return self._accounts
    
    def _load_transactions(self) -> List[TransactionModel]:
        if not hasattr(self, '_transactions'):
            self._load_accounts()
            self._transactions = DatabaseHandler.db_transaction.get_all()
        return self._transactions
    
    def add_bank(self, bank: BankModel) -> None:
        assert isinstance(bank, BankModel)
        existing_bank = next((b for b in self._banks if b.bank_id == bank.bank_id), None)
        if existing_bank:
            raise BankAlreadyExistsError(existing_bank.bank_id)
        self._banks.append(bank)
        DatabaseHandler.db_bank.insert(bank=bank)
        self.load_all_data()
    
    def add_account(self, account: AccountModel) -> None:
        assert isinstance(account, AccountModel)
        existing_account = next((a for a in self._accounts if a.account_id == account.account_id), None)
        if existing_account:
            raise BankAccountAlreadyExistsError(existing_account.account_id)
        self._accounts.append(account)
        DatabaseHandler.db_account.insert(account=account)
        self.load_all_data()
    
    def add_transaction(self, transaction: TransactionModel) -> None:
        assert isinstance(transaction, TransactionModel)
        existing_transaction = next((t for t in self._transactions if t.transaction_id == transaction.transaction_id), None)
        if existing_transaction:
            raise TransactionAlreadyExistsError(existing_transaction.transaction_id)
        self._transactions.append(transaction)
        DatabaseHandler.db_transaction.insert(transaction=transaction)
        self.load_all_data()
        self._execute_transaction(transaction_id=transaction.transaction_id)
    
    def remove_bank(self, bank_id: UUID) -> None:
        assert isinstance(bank_id, UUID)
        bank = next((a for a in self._banks if a.bank_id == bank_id), None)
        if bank:
            self._banks.remove(bank)
            DatabaseHandler.db_bank.delete(bank_id=bank.bank_id)
        self.load_all_data()
    
    def remove_account(self, account_id: UUID) -> None:
        assert isinstance(account_id, UUID)
        account = next((a for a in self._accounts if a.account_id == account_id), None)
        if account:
            self._accounts.remove(account)
            DatabaseHandler.db_account.delete(account_id=account.account_id)
        self.load_all_data()
    
    def remove_transaction(self, transaction_id: UUID) -> None:
        assert isinstance(transaction_id, UUID)
        transaction = next((t for t in self._transactions if t.transaction_id == transaction_id), None)
        if transaction:
            self._undo_execute_transaction(transaction_id=transaction_id)
            self._transactions.remove(transaction)
            DatabaseHandler.db_transaction.delete(transaction_id=transaction.transaction_id)
        self.load_all_data()
    
    def _get_item_by_id(self, items: Iterable, item_id: UUID, id_attr: str) -> Any:
        assert isinstance(item_id, UUID)
        for item in items:
            if getattr(item, id_attr) == item_id:
                return item
        return None
    
    def get_bank(self, bank_id: UUID) -> Optional[BankModel]:
        self.load_all_data()
        return self._get_item_by_id(self._banks, bank_id, 'bank_id')
    
    def get_account(self, account_id: UUID) -> Optional[AccountModel]:
        self.load_all_data()
        return self._get_item_by_id(self._accounts, account_id, 'account_id')
    
    def get_transaction(self, transaction_id: UUID) -> Optional[TransactionModel]:
        self.load_all_data()
        return self._get_item_by_id(self._transactions, transaction_id, 'transaction_id')
    
    @property
    def banks(self) -> List[BankModel]:
        self.load_all_data()
        banks = deepcopy(self._banks)
        return banks
    
    @property
    def accounts(self) -> List[AccountModel]:
        self.load_all_data()
        accounts = deepcopy(self._accounts)
        return accounts
    
    @property
    def transactions(self) -> List[TransactionModel]:
        self.load_all_data()
        transactions = deepcopy(self._transactions)
        return transactions
    
    def _execute_transaction(self, transaction_id: UUID) -> None:
        assert isinstance(transaction_id, UUID)
        transaction = next((t for t in self._transactions if t.transaction_id == transaction_id), None)
        if transaction:
            transaction.execute()
            destination = transaction.destination
            origin = transaction.origin
            self.update_account(account_id=destination.account_id, account=destination)
            if origin:
                self.update_account(account_id=origin.account_id, account=origin)
            self.update_transaction(transaction_id=transaction_id, transaction=transaction)
            self.load_all_data()
        else:
            raise TransactionNotFoundError(transaction_id=transaction_id)
    
    def _undo_execute_transaction(self, transaction_id: UUID) -> None:
        assert isinstance(transaction_id, UUID)
        transaction = next((t for t in self._transactions if t.transaction_id == transaction_id), None)
        if transaction:
            transaction.undo_execute()
            destination = transaction.destination
            origin = transaction.origin
            self.update_account(account_id=destination.account_id, account=destination)
            if origin:
                self.update_account(account_id=origin.account_id, account=origin)
            self.update_transaction(transaction_id=transaction_id, transaction=transaction)
            self.load_all_data()
        else:
            raise TransactionNotFoundError(transaction_id=transaction_id)
    
    def update_bank(self, bank_id: UUID, bank: BankModel) -> None:
        existing_bank = next((b for b in self._banks if b.bank_id == bank.bank_id), None)
        if existing_bank:
            DatabaseHandler.db_bank.update(bank_id=bank_id, bank=bank)
            self.load_all_data()
        else:
            raise BankNotFoundError(bank_id=bank.bank_id)
    
    def update_account(self, account_id: UUID, account: AccountModel) -> None:
        existing_account = next((b for b in self._accounts if b.account_id == account.account_id), None)
        if existing_account:
            DatabaseHandler.db_account.update(account_id=account_id, account=account)
            self.load_all_data()
        else:
            raise BankAccountNotFoundError(account_id=account_id)
    
    def update_transaction(self, transaction_id: UUID, transaction: TransactionModel) -> None:
        existing_transaction = next((b for b in self._transactions if b.transaction_id == transaction.transaction_id), None)
        if existing_transaction:
            DatabaseHandler.db_transaction.update(transaction_id=transaction_id, transaction=transaction)
            self.load_all_data()
        else:
            raise TransactionNotFoundError(transaction_id=transaction_id)




