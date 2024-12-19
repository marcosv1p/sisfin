from datetime import datetime
from typing import Optional, List

from infra.entities import User
from infra.configs import DBConnectionHandler


class UserRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def select(self) -> List[User]:
        with DBConnectionHandler() as db:
            data = db.session\
                .query(User)\
                .all()
            return data
    
    def select_from_id(self, id: str) -> Optional[User]:
        with DBConnectionHandler() as db:
            data = db.session\
                .query(User)\
                .filter(User.id==id)\
                .one_or_none()
            return data
    
    def insert(self, id:str, nickname: str, created_at: datetime) -> User:
        with self.db as db:
            new_user = User(
                id = id,
                nickname = nickname,
                created_at = created_at
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
    
    def update(self, id:str, nickname:str=None, created_at:datetime=None) -> Optional[User]:
        with DBConnectionHandler() as db:
            user = db.session.query(User).filter(User.id == id).one_or_none()
            if user:
                if nickname:
                    user.nickname = nickname
                if created_at:
                    user.created_at = created_at
                db.session.commit()
                return self.select_from_id(id=id)
            return None
    
    def delete(self, id: str) -> None:
        with DBConnectionHandler() as db:
            db.session.query(User).filter(User.id == id).delete()
            db.session.commit()
