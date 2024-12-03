from datetime import datetime
from typing import Optional, List

from infra.entities.user import User
from infra.configs.connection import DBConnectionHandler


class UserRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def select(self) -> List[User]:
        with DBConnectionHandler() as db:
            data = db.session\
                .query(User)\
                .all()
            return data
    
    def select_from_id(self, user_id: str) -> Optional[User]:
        with DBConnectionHandler() as db:
            data = db.session\
                .query(User)\
                .filter(User.user_id==user_id)\
                .one_or_none()
            return data
    
    def select_from_nickname(self, nickname: str) -> Optional[User]:
        with DBConnectionHandler() as db:
            data = db.session\
                .query(User)\
                .filter(User.nickname==nickname)\
                .one_or_none()
            return data
    
    def insert(self, user_id:str, nickname: str, created_at: datetime) -> User:
        with self.db as db:
            new_user = User(
                user_id = user_id,
                nickname = nickname,
                created_at = created_at
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
    
    def update(self, user_id:str, nickname: str=None, created_at: datetime=None) -> Optional[User]:
        with DBConnectionHandler() as db:
            user = db.session.query(User).filter(User.user_id == user_id).one_or_none()
            if user:
                if nickname:
                    user.nickname = nickname
                if created_at:
                    user.created_at = created_at
                db.session.commit()
                return self.select_from_id(user_id=user_id)
            return None
    
    def delete(self, user_id: str) -> None:
        with DBConnectionHandler() as db:
            db.session.query(User).filter(User.user_id == user_id).delete()
            db.session.commit()
