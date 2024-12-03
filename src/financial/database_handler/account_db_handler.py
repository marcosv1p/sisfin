from uuid import UUID
from decimal import Decimal
from typing import List, Optional

from infra import AccountRepository
from src.financial.models import AccountModel, UserModel
from src.financial.database_handler.database_handler_interface import DatabaseHandlerInterface
from src.financial.exceptions.database_handler_error import AccountDatabaseHandlerError

class AccountDatabaseHandler(DatabaseHandlerInterface):
    _db = AccountRepository()
    
    @classmethod
    def insert(cls, account: AccountModel) -> None:
        account = cls._db.select_from_id(account.account_id.hex)
        if account:
            raise AccountDatabaseHandlerError("Já existe um 'Account' com mesmo 'account_id' no banco de dados")
        cls._db.insert(
            account_id=account.account_id.hex,
            name=account.name,
            description=account.description,
            balance=account.balance,
            created_at=account.created_at,
            created_by=account.created_by,
        )
    
    @classmethod
    def update(cls, account_id: UUID, account: AccountModel) -> None:
        current_account = cls._db.select_from_id(account_id=account_id.hex)
        
        if not current_account:
            raise AccountDatabaseHandlerError("Conta não encontrada.")
        
        updates = {}
        
        if account.account_id and account.account_id != UUID(current_account.account_id):
            raise AccountDatabaseHandlerError("Incosistencia entre o parametro 'account_id' e a proprienda account_id do paramentro 'account'")
        
        if account.name and account.name != current_account.name:
            updates['name'] = account.name
        
        if account.description and account.description != current_account.description:
            updates['description'] = account.description
        
        if account.balance and account.balance != Decimal(current_account.balance):
            updates['balance'] = account.balance
        
        if account.created_at and account.created_at != current_account.created_at:
            updates['created_at'] = account.created_at
        
        if account.created_by and account.created_by.hex != current_account.created_by:
            updates['created_by'] = account.created_by.hex
        
        if updates:
            result = cls._db.update(
                account_id=account_id,
                name=updates.get("name"),
                description=updates.get("description"),
                balance=updates.get("balance"),
                created_at=updates.get("created_at"),
                created_by=updates.get("created_by"),
            )
            if not result:
                raise AccountDatabaseHandlerError("Falha ao tentar atualizar 'Account'")
    
    @classmethod
    def delete(cls, account_id: UUID) -> None:
        cls._db.delete(account_id=account_id.hex)
    
    @classmethod
    def get(cls, account_id: UUID) -> Optional[AccountModel]:
        data = cls._db.select_from_id(account_id=account_id.hex)
        if data:
            return AccountModel(
                account_id=UUID(data.account_id),
                name=data.name,
                description=data.description,
                balance=Decimal(data.balance),
                created_at=data.created_at,
                created_by=UUID(data.created_by),
            )
        return None
    
    @classmethod
    def get_all(cls) -> List[AccountModel]:
        data = cls._db.select()
        if data:
            result = []
            for account in data:
                result.append(
                    AccountModel(
                        account_id=UUID(account.account_id),
                        name=data.name,
                        description=data.description,
                        balance=Decimal(data.balance),
                        created_at=data.created_at,
                        created_by=UUID(data.created_by),
                    )
                )
            return result
        return []
