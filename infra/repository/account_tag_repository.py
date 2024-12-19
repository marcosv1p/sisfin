from datetime import datetime
from typing import Optional, List

from infra.entities import AccountTag
from infra.configs import DBConnectionHandler


class AccountTagRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def select(self) -> List[AccountTag]:
        with self.db as db:
            data = db.session\
                .query(AccountTag)\
                .all()
        return data
    
    def select_from_id(self, id: str) -> Optional[AccountTag]:
        with self.db as db:
            return db.session\
                .query(AccountTag)\
                .filter(AccountTag.id == id)\
                .one_or_none()
    
    def insert(self,
            id: str,
            name: str,
            created_at: datetime,
            user_id: str) -> AccountTag:
        with self.db as db:
            new_account_tag = AccountTag(
                id=id,
                name=name,
                created_at=created_at,
                user_id=user_id,
            )
            db.session.add(new_account_tag)
            db.session.commit()
            return new_account_tag
    
    def update(self, id: str = None,
            name: str = None,
            created_at: datetime = None,
            user_id: str = None) -> Optional[AccountTag]:
        with self.db as db:
            account_tag = db.session\
                .query(AccountTag)\
                .filter(AccountTag.id == id)\
                .one_or_none()
            
            if not account_tag:
                return None
            
            fields_to_update = {
                "name": name,
                "created_at": created_at,
                "user_id": user_id,
            }
            
            for field, value in fields_to_update.items():
                if value is not None:
                    setattr(account_tag, field, value)
            
            db.session.commit()
            
            return self.select_from_id(id=id)
    
    def delete(self, id: str) -> None:
        with self.db as db:
            db.session.query(AccountTag).filter(AccountTag.id == id).delete()
            db.session.commit()
