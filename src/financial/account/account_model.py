import re

from pydantic import BaseModel, Field, constr, condecimal
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from typing import Any

from src.financial.bank import BankModel


class AccountModel(BaseModel):
    bank: UUID
    name: constr(min_length=1, max_length=64, pattern=re.compile(r"^[\w\s\-\.:çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)) = Field(default_factory=lambda: uuid4().hex)
    description: constr(max_length=255, pattern=re.compile(r"^[\w\s\-\.:çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)) = Field(default=None)
    balance: condecimal(decimal_places=2) = Field(default=Decimal("0.00"))
    
    account_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    
    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


