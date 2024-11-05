from uuid import UUID
from typing import List
from decimal import Decimal
from datetime import datetime

from infra import TransactionRepository
from src.financial.transaction import TransactionModel
from src.financial.account import AccountModel
from src.financial.database_handler.account_handler import AccountDatabaseHandler


class TransactionDatabaseHandler:
    _db = TransactionRepository()
    
    @classmethod
    def insert(cls, transaction: TransactionModel) -> None:
        """Insere uma nova transação no banco de dados."""
        result = cls._db.select_from_id(transaction.transaction_id.hex)
        if result:
            cls._db.delete(account_id=transaction.account_id.hex)
        cls._db.insert(
            transaction_id=transaction.transaction_id.hex,
            date=transaction.date,
            description=transaction.description,
            value=transaction.value,
            transaction_type=transaction.transaction_type.value,
            origin=transaction.origin.account_id.hex if transaction.origin else None,
            destination=transaction.destination.account_id.hex,
            status=transaction.status,
            created_at=transaction.created_at
        )
    
    @classmethod
    def update(cls, transaction_id: UUID, transaction: TransactionModel) -> None:
        """Atualiza os dados de uma transação existente apenas com os campos alterados."""
        
        # Obter os dados atuais da transação
        current_transaction = cls._db.select_from_id(transaction_id=transaction_id.hex)
        
        if not current_transaction:
            raise ValueError("Transação não encontrada.")
        
        # Dicionário para campos modificados
        updates = {}
        if transaction.transaction_id and transaction.transaction_id != transaction.transaction_id:
            updates['transaction_id'] = transaction.transaction_id.hex
        
        # Comparar e adicionar campos alterados ao dicionário `updates`
        if transaction.description and transaction.description != current_transaction.description:
            updates['new_description'] = transaction.description
        
        if transaction.value and transaction.value != current_transaction.value:
            updates['new_value'] = transaction.value
        
        if transaction.transaction_type and transaction.transaction_type.value != current_transaction.transaction_type:
            updates['new_transaction_type'] = transaction.transaction_type.value
        
        if transaction.origin and transaction.origin.account_id.hex != (current_transaction.origin if current_transaction.origin else None):
            updates['new_origin'] = transaction.origin.account_id.hex
        elif not transaction.origin:
            updates['new_origin'] = None  # Remove a origem se não estiver definida
        
        if transaction.destination and transaction.destination.account_id.hex != current_transaction.destination:
            updates['new_destination'] = transaction.destination.account_id.hex
        
        if transaction.status is not None and transaction.status != current_transaction.status:
            updates['new_status'] = transaction.status
        
        # Executa o update apenas se houver campos alterados
        if updates:
            cls._db.update(transaction_id=transaction_id, **updates)
    
    @classmethod
    def delete(cls, transaction_id: UUID) -> None:
        """Deleta uma transação com base no ID fornecido."""
        cls._db.delete(transaction_id=transaction_id.hex)
    
    @classmethod
    def get(cls, transaction_id: UUID) -> TransactionModel:
        """Obtém uma conta bancária pelo ID."""
        raw_data = cls._db.select_from_id(transaction_id=transaction_id.hex)
        if raw_data:
            data = raw_data.to_dict()
            data.update(
                date=datetime.fromisoformat(data.get("date")),
                value=Decimal(data.get("value")),
                origin=AccountDatabaseHandler.get(UUID(data.get("origin"))) if data.get("origin") else None,
                destination=AccountDatabaseHandler.get(UUID(data.get("destination"))),
                transaction_id=transaction_id,
                created_at=datetime.fromisoformat(data.get("created_at")),
                )
            return TransactionModel(**data)
        return None
    
    @classmethod
    def get_all(cls) -> List[TransactionModel]:
        """Obtém todas as transações."""
        raw_data = cls._db.select()
        if raw_data:
            data = []
            for transaction in raw_data:
                data.append(cls.get(transaction_id=UUID(transaction.transaction_id)))
            return data
        return []
