from datetime import datetime
from typing import Optional, List

from infra.entities.user import User
from infra.entities.transaction import Transaction
from infra.configs.connection import DBConnectionHandler


class TransactionRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def select(self) -> List[Transaction]:
        with self.db as db:
            data = db.session\
            .query(Transaction)\
            .all()
        return data
    
    def select_from_id(self, transaction_id: str) -> Optional[Transaction]:
        with self.db as db:
            return db.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).one_or_none()
    
    def insert(self, transaction_id: str, date: datetime, description: str, amount: float, transaction_type: str, status: bool, calculate: bool, created_at: datetime, created_by: User,  origin: Optional[str], destination: str) -> Transaction:
        with self.db as db:
            new_transaction = Transaction(
                transaction_id=transaction_id,
                date=date,
                description=description,
                amount=amount,
                transaction_type=transaction_type,
                status=status,
                calculate=calculate,
                created_at=created_at,
                created_by=created_by,
                origin=origin,
                destination=destination,
            )
            db.session.add(new_transaction)
            db.session.commit()
            return new_transaction
    
    def update(self, transaction_id: str, date: datetime=None, description: str=None, amount: float=None, transaction_type: str=None, status: bool=None, calculate: bool=None, created_at: datetime=None, created_by: User=None,  origin: Optional[str]=None, destination: str=None) -> Optional[Transaction]:
        with self.db as db:
            transaction = db.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).one_or_none()
            if transaction:
                if date:
                    transaction.date = date
                if description:
                    transaction.description = description
                if amount:
                    transaction.value = amount
                if transaction_type:
                    transaction.transaction_type = transaction_type
                if status:
                    transaction.status = status
                if calculate:
                    transaction.calculate = calculate
                if created_at:
                    transaction.created_at = created_at
                if created_by:
                    transaction.created_by = created_by
                if origin:
                    transaction.origin = origin
                if destination:
                    transaction.destination = destination
                db.session.commit()
                return self.select_from_id(transaction_id=transaction_id)
            return None
    
    def delete(self, transaction_id: str) -> None:
        """Deleta uma transação com base no ID fornecido.
        
        Args:
            transaction_id (str): O ID da transação a ser deletada.
        """
        with self.db as db:
            db.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).delete()
            db.session.commit()
