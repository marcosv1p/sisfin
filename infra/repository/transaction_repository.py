from datetime import datetime
from typing import Optional, List

from infra.entities import Transaction
from infra.configs import DBConnectionHandler


class TransactionRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def select(self) -> List[Transaction]:
        with self.db as db:
            data = db.session\
            .query(Transaction)\
            .all()
        return data
    
    def select_from_id(self, id: str) -> Optional[Transaction]:
        with self.db as db:
            return db.session\
                .query(Transaction)\
                .filter(Transaction.id == id)\
                .one_or_none()
    
    def insert(self,
            id: str,
            date: datetime,
            description: str,
            amount: float,
            transaction_type: str,
            paid: bool,
            ignore: bool,
            visible: bool,
            category_id: str,
            tag_id: str,
            account_id_origin: Optional[str],
            account_id_destination: str,
            created_at: datetime,
            user_id: str) -> Transaction:
        with self.db as db:
            new_transaction = Transaction(
                id=id,
                date=date,
                description=description,
                amount=amount,
                transaction_type=transaction_type,
                paid=paid,
                ignore=ignore,
                visible=visible,
                category_id=category_id,
                tag_id=tag_id,
                account_id_origin=account_id_origin,
                account_id_destination=account_id_destination,
                created_at=created_at,
                user_id=user_id,
            )
            db.session.add(new_transaction)
            db.session.commit()
            return new_transaction
    
    def update(self,
            id: str,
            date: datetime = None,
            description: str = None,
            amount: float = None,
            transaction_type: str = None,
            paid: bool = None,
            ignore: bool = None,
            visible: bool = None,
            category_id: str = None,
            tag_id: str = None,
            account_id_origin: Optional[str] = None,
            account_id_destination: str = None,
            created_at: datetime = None,
            user_id: str = None) -> Optional[Transaction]:
        with self.db as db:
            transaction = db.session.query(Transaction).filter(Transaction.id == id).one_or_none()
            
            if transaction:
                return None
            
            fields_to_update = {
                "date": date,
                "description": description,
                "amount": amount,
                "transaction_type": transaction_type,
                "paid": paid,
                "ignore": ignore,
                "visible": visible,
                "category_id": category_id,
                "tag_id": tag_id,
                "account_id_origin": account_id_origin,
                "account_id_destination": account_id_destination,
                "created_at": created_at,
                "user_id": user_id,
            }
            
            for field, value in fields_to_update.items():
                if value is not None:  # Só atualiza se o valor não for None
                    setattr(transaction, field, value)
            db.session.commit()
            
            return self.select_from_id(id=id)
    
    def delete(self, id: str) -> None:
        with self.db as db:
            db.session.query(Transaction).filter(Transaction.id == id).delete()
            db.session.commit()
