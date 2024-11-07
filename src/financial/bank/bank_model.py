import re

from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, AnyUrl, constr
from typing import Any, Optional


class BankModel(BaseModel):
    """
    Representa um banco com informações básicas, incluindo nome, descrição e imagem.
    
    ### Atributos:
    - **name** (`str`): Nome do banco, com comprimento entre 1 e 64 caracteres. Aceita letras, números, espaços e caracteres especiais (e.g., "- . : ç Ç á Á"), mas **sem vírgulas**.
    - **description** (`str`, opcional): Descrição adicional sobre o banco, com até 255 caracteres e suportando os mesmos caracteres especiais do `name` mais a vírgula.
    - **url_image** (`AnyUrl`, opcional): URL de uma imagem representando o banco (ex. logotipo ou símbolo).
    - **bank_id** (`UUID`): Identificador único do banco, gerado automaticamente ao criar uma nova instância.
    - **created_at** (`datetime`): Data e hora de criação do banco, inicializada automaticamente ao instanciar o modelo.
    """
    # `name` não permite vírgulas
    name: constr(
        min_length=1, max_length=64,
        pattern=re.compile(r"^[\w\s\-\çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)
    )
    
    # `description` permite vírgulas
    description: constr(
        max_length=255,
        pattern=re.compile(r"^[\w\s\-\.,:çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)
    ) = Field(default=None)
    
    url_image: Optional[AnyUrl] = Field(default=None)
    bank_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    
    def update(self, **kwargs: Any) -> "BankModel":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"O atributo '{key}' não existe na classe BankModel.")
        return self
