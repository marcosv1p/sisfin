from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Float

from infra.configs import Base


class Account(Base):
    __tablename__ = "accounts"
    
    account_id = Column(String(64), primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)
    balance = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(String(64), ForeignKey("user.user_id"), nullable=False)
    
    user = relationship("User")
    
    def __repr__(self):
        return (f"<Account(account_id='{self.account_id}', name='{self.name}', "
                f"description='{self.description}', created_at='{self.created_at}', "
                f"created_by='{self.created_by}')>")