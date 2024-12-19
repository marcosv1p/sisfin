from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Boolean

from infra.configs import Base


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String(64), primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(64), nullable=False)
    paid = Column(Boolean, nullable=False)
    ignore = Column(Boolean, nullable=False)
    visible = Column(Boolean, nullable=False)
    category_id = Column(String(64), ForeignKey("transactions_categories.id"), nullable=False)
    tag_id = Column(String(64), ForeignKey("transactions_tags.id"), nullable=False)
    account_id_origin = Column(String(64), ForeignKey("accounts.id"))
    account_id_destination = Column(String(64), ForeignKey("accounts.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    user_id = Column(String(64), ForeignKey("users.id"), nullable=False)
    
    # def __repr__(self):
    #     return (f"<Transaction(transaction_id='{self.transaction_id}', date='{self.date}', "
    #             f"description='{self.description}', amount={self.amount}, transaction_type='{self.transaction_type}', "
    #             f"status={self.status}, calculate='{self.calculate}', created_at='{self.created_at}', "
    #             f"created_by='{self.created_by}', origin='{self.origin}', destination='{self.destination}')>")
