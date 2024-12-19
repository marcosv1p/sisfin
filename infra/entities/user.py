from sqlalchemy import Column, String, DateTime

from infra.configs import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(String(64), primary_key=True, nullable=False)
    nickname = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    # def __repr__(self):
    #     return f"<User(user_id='{self.user_id}', nickname='{self.nickname}', created_at='{self.created_at}')>"
