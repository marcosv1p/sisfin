from uuid import UUID
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from infra.configs import Base


class Transaction(Base):
    __tablename__ = "transaction"  # Corrigido o nome da tabela
    
    transaction_id = Column(String(64), primary_key=True, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    description = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    transaction_type = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(Boolean, default=True, nullable=False)  # Novo campo status
    
    origin = Column(String(64), ForeignKey("bank_account.account_id"))
    destination = Column(String(64), ForeignKey("bank_account.account_id"), nullable=False)
    
    account_origin = relationship(
        "BankAccount",
        foreign_keys=[origin]
    )
    account_destination = relationship(
        "BankAccount",
        foreign_keys=[destination]
    )
    
    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "date": self.date.isoformat(),
            "description": self.description,
            "value": f"{self.value:.2f}",
            "transaction_type": self.transaction_type,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "origin": self.origin if self.origin else None,
            "destination": self.destination
        }
    
    def __repr__(self):
        return (f"<Transaction(transaction_id='{self.transaction_id}', date='{self.date}', "
                f"description='{self.description}', value={self.value}, "
                f"status={self.status}, created_at='{self.created_at}', transaction_type='{self.transaction_type}')>")
