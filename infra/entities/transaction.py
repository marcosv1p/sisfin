from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Boolean

from infra.configs import Base


class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(String(64), primary_key=True, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False) # Troquei de value para amount
    transaction_type = Column(String(64), nullable=False)
    status = Column(Boolean, default=False, nullable=False)
    calculate = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    created_by = Column(String(64), ForeignKey("users.user_id"), nullable=False)
    origin = Column(String(64), ForeignKey("accounts.account_id"))
    destination = Column(String(64), ForeignKey("accounts.account_id"), nullable=False)
    
    def __repr__(self):
        return (f"<Transaction(transaction_id='{self.transaction_id}', date='{self.date}', "
                f"description='{self.description}', amount={self.amount}, transaction_type='{self.transaction_type}', "
                f"status={self.status}, calculate='{self.calculate}', created_at='{self.created_at}', "
                f"created_by='{self.created_by}', origin='{self.origin}', destination='{self.destination}')>")
