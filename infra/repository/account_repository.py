from datetime import datetime
from typing import Optional, List

from infra.entities import Account
from infra.configs import DBConnectionHandler


class AccountRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def select(self) -> List[Account]:
        with self.db as db:
            data = db.session\
                .query(Account)\
                .all()
        return data
    
    def select_from_id(self, id: str) -> Optional[Account]:
        with self.db as db:
            return db.session\
                .query(Account)\
                .filter(Account.id == id)\
                .one_or_none()
    
    def insert(self,
            id: str,
            name: str,
            description: str,
            tag_id: str,
            balance: float,
            created_at: datetime,
            user_id: str) -> Account:
        with self.db as db:
            new_account = Account(
                id=id,
                name=name,
                description=description,
                tag_id=tag_id,
                balance=balance,
                created_at=created_at,
                user_id=user_id,
            )
            db.session.add(new_account)
            db.session.commit()
            return new_account
    
    def update(self,
            id: str = None,
            name: str = None,
            description: str = None,
            tag_id: str = None,
            balance: float = None,
            created_at: datetime = None,
            user_id: str = None) -> Optional[Account]:
        with self.db as db:
            account = db.session.query(Account).filter(Account.id == id).one_or_none()
            
            if not account:
                return None
            
            fields_to_update = {
                "name": name,
                "description": description,
                "tag_id": tag_id,
                "balance": balance,
                "created_at": created_at,
                "user_id": user_id,
            }
            
            for field, value in fields_to_update.items():
                if value is not None:
                    setattr(account, field, value)
            
            db.session.commit()
            
            return self.select_from_id(id=id)
    
    def delete(self, id: str) -> None:
        with self.db as db:
            db.session.query(Account).filter(Account.id == id).delete()
            db.session.commit()
