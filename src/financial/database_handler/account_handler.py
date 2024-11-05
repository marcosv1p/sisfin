from uuid import UUID
from typing import List
from decimal import Decimal
from datetime import datetime

from infra import BankAccountRepository
from src.financial.account import AccountModel

class AccountDatabaseHandler:
    _db = BankAccountRepository()
    
    @classmethod
    def insert(cls, account: AccountModel) -> None:
        """Insere uma nova conta bancária no banco de dados."""
        result = cls._db.select_from_id(account.account_id.hex)
        if result:
            cls._db.delete(account_id=account.account_id.hex)
        cls._db.insert(
            account_id=account.account_id.hex,
            name=account.name,
            description=account.description,
            balance=account.balance,
            bank_id=account.bank.hex,
            created_at=account.created_at
        )
    
    @classmethod
    def update(cls, account_id: UUID, account: AccountModel) -> None:
        """Atualiza os dados de uma conta bancária existente."""
        # Obtenha os dados atuais da conta
        current_account = cls._db.select_from_id(account_id=account_id.hex)
        
        # Se a conta não foi encontrada, talvez retornar uma exceção ou fazer outro tratamento
        if not current_account:
            raise ValueError("Conta bancária não encontrada.")
        
        # Comparar os campos para ver quais mudaram
        updates = {}
        if account.account_id and account.account_id != UUID(current_account.account_id):
            updates['new_account_id'] = account.account_id.hex
        
        if account.name and account.name != current_account.name:
            updates['new_name'] = account.name
        
        if account.description and account.description != current_account.description:
            updates['new_description'] = account.description
        
        if account.created_at and account.created_at != current_account.created_at:
            updates['new_created_at'] = account.created_at
        
        if account.balance and account.balance != current_account.balance:
            updates['new_balance'] = account.balance
        
        if account.bank and account.bank != UUID(current_account.bank_id):
            updates['new_bank_id'] = account.bank.hex
        
        # Executar o update se houver algo para atualizar
        if updates:
            cls._db.update(account_id=account_id, **updates)
    
    @classmethod
    def delete(cls, account_id: UUID) -> None:
        """Deleta uma conta bancária com base no ID fornecido."""
        cls._db.delete(account_id=account_id.hex)
    
    @classmethod
    def get(cls, account_id: UUID) -> AccountModel:
        """Obtém uma conta bancária pelo ID."""
        raw_data = cls._db.select_from_id(account_id=account_id.hex)
        if raw_data:
            data = raw_data.to_dict()
            data.update(
                account_id=account_id,
                balance=Decimal(data.get("balance")),
                bank=UUID(data.get("bank")),
                created_at=datetime.fromisoformat(data.get("created_at")),
                )
            return AccountModel(**data)
        return None
    
    @classmethod
    def get_all(cls) -> List[AccountModel]:
        """Obtém todas as contas bancárias."""
        raw_data = cls._db.select()
        if raw_data:
            data = []
            for account in raw_data:
                data.append(cls.get(account_id=UUID(account.account_id)))
            return data
        return []
