from enum import Enum
from typing import Optional
from decimal import Decimal
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import Field, BaseModel

from src.financial.interfaces import DataInterface


class TransactionCategoryModel(DataInterface):
    # UUID da categoria
    id: UUID = Field(default_factory=uuid4)
    
    # Nome da categoria
    name: str
    
    # Data de criação da categoria
    created_at: datetime = Field(default_factory=datetime.now)
    
    # UUID do usuario que criou que pertense a categoria
    user_id: UUID
    
    def get_current_dict_data(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "created_at": self.created_at,
            "user_id": str(self.user_id)
        }


class TransactionTypes(Enum):
    EXPENSE = "despesa"
    INCOME = "renda"
    TRANSFER = "transferência"
    ADJUST = "ajuste"


class TransactionModel(BaseModel):
    # UUID da trasação
    id: UUID = Field(default_factory=uuid4)
    
    # Data da trasação
    date: datetime = Field(default_factory=datetime.now)
    
    # Descrição da trasação com filtro de caracteres usando expressões regulares
    description: str = Field(default=str())
    
    # Valor de trasação
    amount: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    
    # Tipo da trasação 
    transaction_type: TransactionTypes
    
    # Se já esta pago ou pendente
    paid: bool = Field(default=True)
    
    # Se esta transação deve ser ignorada para balaços e calculos futuros
    ignore: bool = Field(default=False)
    
    # Se essa trasação vai ser visivel ao usuario ou vai ser usada somente para registros
    visible: bool = Field(default=True)
    
    # Categoria da trasação
    category_id: UUID
    
    # Marcação da trasação para melhor organização
    tag_id: Optional[UUID] = Field(default=None)
    
    # UUID da conta de origem de trasação caso for transferencia
    account_id_origin: Optional[UUID] = Field(default=None)
    
    # UUID da conta de destino da trasação
    account_id_destination: UUID
    
    # Data de criação da transação
    created_at: datetime = Field(default_factory=datetime.now)
    
    # UUID do usuario que criou que pertense a trasação
    user_id: UUID
    
    def heve_tag(self):
        return (self.tag_id is not None)
    
    def have_account_id_origin(self):
        return (self.account_id_origin is not None)
    
    def is_transactiontype(self, transaction_type: TransactionTypes):
        return isinstance(self.transaction_type, transaction_type)
    
    def is_visible(self):
        return self.visible
    
    def is_ignored(self):
        return self.ignore
    
    def is_paid(self):
        return self.paid
    
    def update(self, **kwargs) -> "TransactionModel":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"O atributo '{key}' não existe na classe TransactionModel.")
            return self
    
    def get_current_dict_data(self) -> dict:
        return {
            "id": self.id.hex,
            "date": self.date,
            "description": self.description,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "paid": self.paid,
            "ignore": self.ignore,
            "visible": self.visible,
            "category_id": self.category_id.hex,
            "tag_id": self.tag_id.hex,
            "account_id_origin": self.account_id_origin,
            "account_id_destination": self.account_id_destination,
            "created_at": self.created_at,
            "user_id": self.user_id.hex,
        }
