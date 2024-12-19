from sqlalchemy import Column, String, DateTime, ForeignKey

from infra.configs import Base


class TransactionCategory(Base):
    __tablename__ = "transactions_categories"
    
    id = Column(String(64), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    user_id = Column(String(64), ForeignKey("users.id"), nullable=False)