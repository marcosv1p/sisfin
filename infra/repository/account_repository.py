from datetime import datetime
from typing import Optional, List

from infra.entities.user import User
from infra.entities.account import Account
from infra.configs.connection import DBConnectionHandler


class AccountRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def select(self) -> List[Account]:
        with self.db as db:
            data = db.session\
                .query(Account)\
                .all()
        return data
    
    def select_from_id(self, account_id: str) -> Optional[Account]:
        with self.db as db:
            return db.session.query(Account).filter(Account.account_id == account_id).one_or_none()
    
    def insert(self, account_id: str, name: str, description: str, balance: float, created_at: datetime, created_by: User ) -> Account:
        with self.db as db:
            new_account = Account(
                account_id=account_id,
                name=name,
                description=description,
                balance=balance,
                created_at=created_at,
                created_by=created_by,
            )
            db.session.add(new_account)
            db.session.commit()
            return new_account
    
    def update(self, account_id: str, name: str, description: str, balance: float, created_at: datetime, created_by: User) -> Optional[Account]:
        with self.db as db:
            account = db.session.query(Account).filter(Account.account_id == account_id).one_or_none()
            if account:
                if name:
                    account.name = name
                if description:
                    account.description = description
                if balance:
                    account.balance = balance
                if created_at:
                    account.created_at = created_at
                if created_by:
                    account.created_by = created_by
                db.session.commit()
                return self.select_from_id(account_id=account_id)
            return None
    
    def delete(self, account_id: str) -> None:
        with self.db as db:
            db.session.query(Account).filter(Account.account_id == account_id).delete()
            db.session.commit()
