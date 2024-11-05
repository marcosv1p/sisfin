import re

from decimal import Decimal
from uuid import UUID, uuid4
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, PrivateAttr, Field, constr, condecimal

from src.financial.account import AccountModel
from src.financial.transaction import TransactionsTypes


class TransactionModel(BaseModel):
    date: datetime = Field(default_factory=datetime.now)
    description: constr(max_length=255, pattern=re.compile(r"^[\w\s\-\.:çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)) = Field(default=None)
    value: condecimal(decimal_places=2) = Field(default=Decimal("0.00"))
    origin: Optional[AccountModel] = Field(default=None)
    transaction_type: TransactionsTypes
    destination: AccountModel
    
    transaction_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    status: bool = Field(default=False)
    
    def update(self, **kwargs: Any) -> "TransactionModel":
        updated_data = self.model_dump()
        updated_data.update(kwargs)
        return TransactionModel(**updated_data)
    
    def execute(self) -> None:
        if not self.status:
            match self.transaction_type:
                case TransactionsTypes.DEPOSIT:
                    self.destination.update(balance=(self.destination.balance + self.value))
                case TransactionsTypes.WITHDRAW:
                    self.destination.update(balance=self.destination.balance - self.value)
                case TransactionsTypes.TRANSFER:
                    if not self.origin:
                        raise ValueError("Origin account is required for transfer")
                    self.origin.update(balance=(self.origin.balance - self.value))
                    self.destination.update(balance=(self.destination.balance + self.value))
                case _:
                    raise ValueError("Invalid transaction type")
            self.status = True
        else:
            raise ValueError("Transaction already executed")
    
    def undo_execute(self)  -> None:
        if self.status:
            match self.transaction_type:
                case TransactionsTypes.DEPOSIT:
                    self.destination.update(balance=(self.destination.balance - self.value))
                case TransactionsTypes.WITHDRAW:
                    self.destination.update(balance=(self.destination.balance + self.value))
                case TransactionsTypes.TRANSFER:
                    if not self.origin:
                        raise ValueError("Origin account is required for transfer")
                    self.origin.update(balance=(self.origin.balance + self.value))
                    self.destination.update(balance=(self.destination.balance - self.value))
                case _:
                    raise ValueError("Invalid transaction type")
            self.status = False
        else:
            raise ValueError("Transaction already executed")

