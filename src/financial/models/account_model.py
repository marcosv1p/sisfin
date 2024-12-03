import re

from typing import Any
from decimal import Decimal
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, constr, condecimal


class AccountModel(BaseModel):
    account_id: UUID = Field(default_factory=uuid4)
    name: constr(
        min_length=1, max_length=64,
        pattern=re.compile(r"^[\w\s\-\çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)
    ) = Field(default_factory=lambda: uuid4().hex)
    description: constr(
        max_length=255,
        pattern=re.compile(r"^[\w\s\-\.,:çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)
    ) = Field(default=None)
    balance: condecimal(decimal_places=2) = Field(default=Decimal("0.00"))
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: UUID
    
    def update(self, **kwargs: Any) -> "AccountModel":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"O atributo '{key}' não existe na classe AccountModel.")
        return self



