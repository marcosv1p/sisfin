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
        """
        Insere uma nova conta bancária no banco de dados. Se a conta já existir, ela é substituída.
        
        ### Parâmetros:
        - **account** (`AccountModel`): Instância de `AccountModel` representando a conta a ser inserida.
        
        ### Comportamento:
        - Verifica se já existe uma conta com o `account_id` fornecido.
        - Se existir, a conta antiga é removida antes de inserir a nova.
        
        ### Exemplo de Uso:
        ```python
        new_account = AccountModel(name="Conta Pessoal", balance=Decimal("1000.00"))
        AccountDatabaseHandler.insert(new_account)
        ```
        """
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
        current_account = cls._db.select_from_id(account_id=account_id.hex)
        
        if not current_account:
            raise ValueError("Conta bancária não encontrada.")
        
        updates = {}
        if account.account_id and account.account_id != UUID(current_account.account_id):
            updates['new_account_id'] = account.account_id.hex
        
        if account.name and account.name != current_account.name:
            updates['new_name'] = account.name
        
        if account.description and account.description != current_account.description:
            updates['new_description'] = account.description
        
        if account.created_at and account.created_at != current_account.created_at:
            updates['new_created_at'] = account.created_at
        
        if account.balance and account.balance != Decimal(current_account.balance):
            updates['new_balance'] = account.balance
        
        if account.bank and account.bank != UUID(current_account.bank_id):
            updates['new_bank_id'] = account.bank.hex
        
        if updates:
            cls._db.update(
                account_id=account_id,
                new_account_id=updates.get("new_account_id"),
                new_name=updates.get("new_name"),
                new_description=updates.get("new_description"),
                new_created_at=updates.get("new_created_at"),
                new_balance=updates.get("new_balance"),
                new_bank_id=updates.get("new_bank_id"),
            )

        # Certifique-se de que a conta foi atualizada
        return cls.get(account_id)  # Retorna a conta atualizada
    
    @classmethod
    def delete(cls, account_id: UUID) -> None:
        """
        Deleta uma conta bancária do banco de dados com base no ID fornecido.
        
        ### Parâmetros:
        - **account_id** (`UUID`): Identificador único da conta a ser deletada.
        
        ### Exemplo de Uso:
        ```python
        AccountDatabaseHandler.delete(UUID("id_da_conta"))
        ```
        """
        cls._db.delete(account_id=account_id.hex)
    
    @classmethod
    def get(cls, account_id: UUID) -> AccountModel:
        """
        Obtém uma instância de `AccountModel` pelo `account_id` fornecido.
        
        ### Parâmetros:
        - **account_id** (`UUID`): Identificador único da conta desejada.
        
        ### Retorno:
        - (`Optional[AccountModel]`): Instância de `AccountModel` correspondente ao `account_id`, ou `None` se a conta não for encontrada.
        
        ### Exemplo de Uso:
        ```python
        account = AccountDatabaseHandler.get(UUID("id_da_conta"))
        ```
        """
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
        """
        Obtém todas as instâncias de `AccountModel` presentes no banco de dados.
        
        ### Retorno:
        - (`List[AccountModel]`): Lista de todas as instâncias de `AccountModel`.
        
        ### Exemplo de Uso:
        ```python
        all_accounts = AccountDatabaseHandler.get_all()
        ```
        """
        raw_data = cls._db.select()
        if raw_data:
            data = []
            for account in raw_data:
                data.append(cls.get(account_id=UUID(account.account_id)))
            return data
        return []
