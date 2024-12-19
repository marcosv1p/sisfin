from datetime import datetime
from typing import Optional, List

from infra.entities import TransactionCategory
from infra.configs import DBConnectionHandler


class TransactionCategoryRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def select(self) -> List[TransactionCategory]:
        with self.db as db:
            data = db.session\
                .query(TransactionCategory)\
                .all()
        return data
    
    def select_from_id(self, id: str) -> Optional[TransactionCategory]:
        with self.db as db:
            return db.session\
                .query(TransactionCategory)\
                .filter(TransactionCategory.id == id)\
                .one_or_none()
    
    def insert(self,
            id: str,
            name: str,
            created_at: datetime,
            user_id: str) -> TransactionCategory:
        with self.db as db:
            new_transaction_category = TransactionCategory(
                id=id,
                name=name,
                created_at=created_at,
                user_id=user_id,
            )
            db.session.add(new_transaction_category)
            db.session.commit()
            return new_transaction_category
    
    def update(self, id: str = None,
            name: str = None,
            created_at: datetime = None,
            user_id: str = None) -> Optional[TransactionCategory]:
        with self.db as db:
            transaction_category = db.session\
                .query(TransactionCategory)\
                .filter(TransactionCategory.id == id)\
                .one_or_none()
            
            if not transaction_category:
                return None
            
            fields_to_update = {
                "name": name,
                "created_at": created_at,
                "user_id": user_id,
            }
            
            for field, value in fields_to_update.items():
                if value is not None:
                    setattr(transaction_category, field, value)
            
            db.session.commit()
            
            return self.select_from_id(id=id)
    
    def delete(self, id: str) -> None:
        with self.db as db:
            db.session.query(TransactionCategory).filter(TransactionCategory.id == id).delete()
            db.session.commit()
