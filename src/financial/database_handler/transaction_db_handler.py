from uuid import UUID
from typing import List, Optional

from infra import TransactionRepository
from src.financial.models import TransactionModel, TransactionsTypes
from src.financial.exceptions.database_handler_error import TransactionDatabaseHandlerError
from src.financial.database_handler.database_handler_interface import DatabaseHandlerInterface


class TransactionDatabaseHandler(DatabaseHandlerInterface):
    _db = TransactionRepository()
    
    @classmethod
    def insert(cls, transaction: TransactionModel) -> None:
        result = cls._db.select_from_id(transaction.transaction_id.hex)
        if result:
            raise TransactionDatabaseHandlerError("Já existe um 'Transaction' com mesmo 'transaction_id' no banco de dados")
        
        cls._db.insert(
            transaction_id=transaction.transaction_id.hex,
            date=transaction.date,
            description=transaction.description,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type.value,
            status=transaction.status,
            calculate=transaction.calculate,
            created_at=transaction.created_at,
            created_by=transaction.created_by.hex,
            origin=transaction.origin.hex if transaction.origin else None,
            destination=transaction.destination.hex,
        )
    
    @classmethod
    def update(cls, transaction_id: UUID, transaction: TransactionModel) -> None:
        current_transaction = cls._db.select_from_id(transaction_id=transaction_id.hex)
        
        if not current_transaction:
            raise TransactionDatabaseHandlerError("Transação não encontrada.")
        
        updates = {}
        
        if transaction.transaction_id and transaction.transaction_id != transaction.transaction_id:
            raise TransactionDatabaseHandlerError("ID DIFERENTE ERRO QUALQUER AQUI NO 'TRANSACTION_HANDLER'")
        
        if transaction.date and transaction.date != current_transaction.date:
            updates['date'] = transaction.date
        
        if transaction.description and transaction.description != current_transaction.description:
            updates['description'] = transaction.description
        
        if transaction.amount and transaction.amount != current_transaction.amount:
            updates['amount'] = transaction.amount
        
        if transaction.transaction_type and transaction.transaction_type.value != current_transaction.transaction_type:
            updates['transaction_type'] = transaction.transaction_type.value
        
        if transaction.status is not None and transaction.status != current_transaction.status:
            updates['status'] = transaction.status
        
        if transaction.calculate is not None and transaction.calculate != current_transaction.calculate:
            updates['calculate'] = transaction.calculate
        
        if transaction.created_at and transaction.created_at != current_transaction.created_at:
            updates['created_at'] = transaction.created_at
        
        if transaction.created_by and transaction.created_by.hex != current_transaction.created_by:
            updates['created_by'] = transaction.created_by
        
        if transaction.origin and transaction.origin.account_id.hex != (current_transaction.origin if current_transaction.origin else None):
            updates['origin'] = transaction.origin.account_id.hex
        
        elif not transaction.origin:
            updates['origin'] = None
        
        if transaction.destination and transaction.destination.account_id.hex != current_transaction.destination:
            updates['destination'] = transaction.destination.account_id.hex
        
        if updates:
            cls._db.update(
                transaction_id=transaction_id.hex,
                date=updates.get('date'),
                description=updates.get("description"),
                amount=updates.get("amount"),
                transaction_type=updates.get("transaction_type"),
                status=updates.get("status"),
                calculate=updates.get("calculate"),
                created_at=updates.get("created_at"),
                created_by=updates.get("created_by"),
                origin=updates.get("origin"),
                destination=updates.get("destination"),
            )
    
    @classmethod
    def delete(cls, transaction_id: UUID) -> None:
        cls._db.delete(transaction_id=transaction_id.hex)
    
    @classmethod
    def get(cls, transaction_id: UUID) -> Optional[TransactionModel]:
        data = cls._db.select_from_id(transaction_id=transaction_id.hex)
        if data:
            return TransactionModel(
                transaction_id=UUID(data.transaction_id),
                date=data.date,
                description=data.description,
                amount=data.amount,
                transaction_type=TransactionsTypes(data.transaction_type),
                status=data.status,
                calculate=data.calculate,
                created_at=data.created_at,
                created_by=data.created_by,
                origin=data.origin,
                destination=data.destination
            )
        return None
    
    @classmethod
    def get_all(cls) -> List[TransactionModel]:
        data = cls._db.select()
        if data:
            result = []
            for transaction in data:
                result.append(
                    TransactionModel(
                        transaction_id=UUID(transaction.transaction_id),
                        date=transaction.date,
                        description=transaction.description,
                        amount=transaction.amount,
                        transaction_type=TransactionsTypes(transaction.transaction_type),
                        status=transaction.status,
                        calculate=transaction.calculate,
                        created_at=transaction.created_at,
                        created_by=transaction.created_by,
                        origin=transaction.origin,
                        destination=transaction.destination
                    )
                )
            return result
        return []
