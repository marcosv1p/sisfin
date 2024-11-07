import re

from typing import Any
from decimal import Decimal
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, constr, condecimal


class AccountModel(BaseModel):
    """
    Modelo de conta bancária representando as informações básicas de uma conta.
    
    ## Atributos
    - `bank` (UUID): Identificador único do banco associado à conta.
    - `name` (str): Nome da conta. Deve ter entre 1 e 64 caracteres, incluindo letras, números, espaços, hífens, pontos e caracteres específicos em português.
    - `description` (str, opcional): Descrição adicional da conta, limitada a 255 caracteres. Inclui letras, números e caracteres especiais permitidos.
    - `balance` (Decimal): Saldo atual da conta, com precisão de duas casas decimais. Valor padrão é 0.00.
    - `account_id` (UUID): Identificador único da conta, gerado automaticamente.
    - `created_at` (datetime): Data e hora de criação da conta, gerada automaticamente.
    
    ## Métodos
    - `update`: Permite atualizar os atributos da conta com novos valores.
    """
    bank: UUID
    name: constr(
        min_length=1, max_length=64,
        pattern=re.compile(r"^[\w\s\-\çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)
    ) = Field(default_factory=lambda: uuid4().hex)
    
    description: constr(
        max_length=255,
        pattern=re.compile(r"^[\w\s\-\.,:çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)
    ) = Field(default=None)
    
    balance: condecimal(decimal_places=2) = Field(default=Decimal("0.00"))
    account_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    
    def update(self, **kwargs: Any) -> "AccountModel":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"O atributo '{key}' não existe na classe AccountModel.")
        return self



