import re

from decimal import Decimal
from uuid import UUID, uuid4
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, constr, condecimal

from src.financial.models.user_model import UserModel
from src.financial.models.enums import TransactionsTypes
from src.financial.models.account_model import AccountModel


class TransactionModel(BaseModel):
    transaction_id: UUID = Field(default_factory=uuid4)
    date: datetime = Field(default_factory=datetime.now)
    description: constr(
        max_length=255,
        pattern=re.compile(r"^[\w\s\-\.,:çÇáÁéÉíÍóÓúÚãÃõÕ]+$",
        re.UNICODE)
    ) = Field(default=str())
    amount: condecimal(decimal_places=2) = Field(default=Decimal("0.00"))
    transaction_type: TransactionsTypes
    status: bool = Field(default=False)
    calculate: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: UUID
    origin: Optional[UUID] = Field(default=None)
    destination: UUID
    
    def update(self, **kwargs: Any) -> "TransactionModel":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"O atributo '{key}' não existe na classe TransactionModel.")
            return self
