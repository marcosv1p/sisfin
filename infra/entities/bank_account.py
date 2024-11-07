from uuid import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Float, ForeignKey, DateTime

from infra.configs import Base


class BankAccount(Base):
    __tablename__ = "bank_account"
    
    account_id = Column(String(64), primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)
    balance = Column(Float, nullable=False)
    bank_id = Column(String(64), ForeignKey("bank.bank_id"), nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    bank = relationship("Bank")
    
    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "name": self.name,
            "description": self.description,
            "balance": f"{self.balance:.2f}",
            "bank": self.bank_id,
            "created_at": self.created_at.isoformat(),
        }
    
    def __repr__(self):
        return f"<BankAccount(account_id={self.account_id}, name={self.name}, balance={self.balance}, bank_id={self.bank_id}, created_at='{self.created_at}')>"
