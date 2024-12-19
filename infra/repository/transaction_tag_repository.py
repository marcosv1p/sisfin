from datetime import datetime
from typing import Optional, List

from infra.entities import TransactionTag
from infra.configs import DBConnectionHandler


class TransactionTagRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def select(self) -> List[TransactionTag]:
        with self.db as db:
            data = db.session\
                .query(TransactionTag)\
                .all()
        return data
    
    def select_from_id(self, id: str) -> Optional[TransactionTag]:
        with self.db as db:
            return db.session\
                .query(TransactionTag)\
                .filter(TransactionTag.id == id)\
                .one_or_none()
    
    def insert(self,
            id: str,
            name: str,
            created_at: datetime,
            user_id: str) -> TransactionTag:
        with self.db as db:
            new_transaction_tag = TransactionTag(
                id=id,
                name=name,
                created_at=created_at,
                user_id=user_id,
            )
            db.session.add(new_transaction_tag)
            db.session.commit()
            return new_transaction_tag
    
    def update(self, id: str = None,
            name: str = None,
            created_at: datetime = None,
            user_id: str = None) -> Optional[TransactionTag]:
        with self.db as db:
            transaction_tag = db.session\
                .query(TransactionTag)\
                .filter(TransactionTag.id == id)\
                .one_or_none()
            
            if not transaction_tag:
                return None
            
            fields_to_update = {
                "name": name,
                "created_at": created_at,
                "user_id": user_id,
            }
            
            for field, value in fields_to_update.items():
                if value is not None:
                    setattr(transaction_tag, field, value)
            
            db.session.commit()
            
            return self.select_from_id(id=id)
    
    def delete(self, id: str) -> None:
        with self.db as db:
            db.session.query(TransactionTag).filter(TransactionTag.id == id).delete()
            db.session.commit()
