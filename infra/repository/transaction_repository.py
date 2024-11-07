from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import joinedload

from infra.entities.transaction import Transaction
from infra.configs.connection import DBConnectionHandler


class TransactionRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def insert(self, transaction_id: str, date: datetime, description: str, value: float, transaction_type: str, origin: Optional[str], destination: str, status: bool, created_at: datetime) -> Transaction:
        """Insere uma nova transação no banco de dados.
        
        Args:
            transaction_id (str): O ID da transação.
            date (datetime): A data da transação.
            description (str): A descrição da transação.
            value (float): O valor da transação.
            transaction_type (str): O tipo da transação.
            origin (str): O ID da conta de origem.
            destination (str): O ID da conta de destino.
            status (bool): O status da transação (ativo ou inativo). Defaults to True.
        
        Retorna:
            str: O ID da transação recém-criada.
        """
        with self.db as db:
            new_transaction = Transaction(
                transaction_id=transaction_id,
                date=date,
                description=description,
                value=value,
                transaction_type=transaction_type,
                origin=origin,
                destination=destination,
                status=status,
                created_at=created_at
            )
            db.session.add(new_transaction)
            db.session.commit()
            return new_transaction
    
    def select(self) -> List[Transaction]:
        """Consulta todas as transações no banco de dados.
        
        Retorna:
            list: Uma lista de todas as transações.
        """
        with self.db as db:
            data = db.session\
            .query(Transaction)\
            .options(joinedload(Transaction.account_origin), joinedload(Transaction.account_destination))\
            .all()
        return data
    
    def select_from_id(self, transaction_id: str) -> Optional[Transaction]:
        """Consulta uma transação pelo ID fornecido.
        
        Args:
            transaction_id (str): O ID da transação.
        
        Retorna:
            Transaction: A transação correspondente ao ID, ou None se não encontrada.
        """
        with self.db as db:
            return db.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).one_or_none()
    
    def update(self, transaction_id: str, new_transaction_id: str = None, new_date: datetime = None, new_description: str = None, new_value: float = None, new_transaction_type: str = None, new_origin: str = None, new_destination: str = None, new_status: bool = None, new_created_at: datetime = None) -> Optional[Transaction]:
        """Atualiza uma transação com base no ID fornecido.
        
        Args:
            transaction_id (str): O ID da transação a ser atualizada.
            new_description (str, optional): A nova descrição da transação. Defaults to None.
            new_value (float, optional): O novo valor da transação. Defaults to None.
            new_transaction_type (str, optional): O novo tipo da transação. Defaults to None.
            new_origin (str, optional): O novo ID da conta de origem. Defaults to None.
            new_destination (str, optional): O novo ID da conta de destino. Defaults to None.
            new_status (bool, optional): O novo status da transação. Defaults to None.
        
        Retorna:
            Transaction: A transação atualizada, ou None se a transação não foi encontrada.
        """
        with self.db as db:
            transaction = db.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).one_or_none()
            if transaction:
                if new_date:
                    transaction.date = new_date
                if new_description:
                    transaction.description = new_description
                if new_value is not None:
                    transaction.value = new_value
                if new_transaction_type:
                    transaction.transaction_type = new_transaction_type
                if new_origin:
                    transaction.origin = new_origin
                if new_destination:
                    transaction.destination = new_destination
                if new_status is not None:
                    transaction.status = new_status
                if new_created_at:
                    transaction.created_at = new_created_at
                if new_transaction_id:
                    new_transaction = Transaction(
                        transaction_id=new_transaction_id,
                        date=transaction.date,
                        description=transaction.description,
                        value=transaction.value,
                        transaction_type=transaction.transaction_type,
                        origin=transaction.origin,
                        destination=transaction.destination,
                        status=transaction.status,
                        created_at=transaction.created_at
                    )
                    db.session.delete(transaction)
                    db.session.add(new_transaction)
                    transaction_id = new_transaction_id
                db.session.commit()
                return self.select_from_id(transaction_id=new_transaction_id)
            return None
    
    def delete(self, transaction_id: str) -> None:
        """Deleta uma transação com base no ID fornecido.
        
        Args:
            transaction_id (str): O ID da transação a ser deletada.
        """
        with self.db as db:
            db.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).delete()
            db.session.commit()
