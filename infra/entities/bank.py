from uuid import UUID
from sqlalchemy import Column, String, DateTime

from infra.configs import Base


class Bank(Base):
    __tablename__ = "bank"
    
    bank_id = Column(String(64), primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)
    url_image = Column(String(), nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    def to_dict(self) -> dict:
        return {
            "bank_id": self.bank_id,
            "name": self.name,
            "description": self.description,
            "url_image": self.url_image if self.url_image else None,
            "created_at": self.created_at.isoformat(),
        }
    
    def __repr__(self):
        return f"<Bank(bank_id='{self.id}', name='{self.name}', url_image='{self.url_image}', created_at='{self.created_at}')>"
