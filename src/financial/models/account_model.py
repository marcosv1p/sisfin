from typing import Optional
from decimal import Decimal
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import Field, BaseModel


class AccountTagModel(BaseModel):
    # UUID da tag
    id: UUID = Field(default_factory=uuid4)
    
    # Nome da tag
    name: str
    
    # Data de criação da tag
    created_at: datetime = Field(default_factory=datetime.now)
    
    # UUID do usuario que criou que pertense a tag
    user_id: UUID
    
    def get_current_dict_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "user_id": self.user_id
        }


class AccountModel(BaseModel):
    # UUID da conta
    id: UUID = Field(default_factory=uuid4)
    
    # Nome referente a conta
    name: str = Field(default=uuid4().hex)
    
    # Descrição da conta
    description: str = Field(default=None)
    
    # Tag é um marcador para melhor organização da conta
    tag_id: Optional[UUID] = Field(default=None)
    
    # Saldo da conta
    balance: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    
    # Data de criação da conta
    created_at: datetime = Field(default_factory=datetime.now)
    
    # A que usuário pertence a conta
    user_id: UUID
    
    def added_balance(self, amount: Decimal):
        self.balance += amount
    
    def subtract_balance(self, amount: Decimal):
        self.balance -= amount
    
    def have_tag(self):
        return (self.tag_id is not None)
    
    def update(self, **kwargs) -> "AccountModel":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"O atributo '{key}' não existe na classe AccountModel.")
        return self
    
    def get_current_dict_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tag_id": self.tag_id,
            "balance": self.balance,
            "created_at": self.created_at,
            "user_id": self.user_id
        }
