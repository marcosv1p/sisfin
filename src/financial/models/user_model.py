import re

from typing import Any
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, constr

class UserModel(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    nickname: constr(
        min_length=1, max_length=64,
        pattern=re.compile(r"^[\w\s\-\çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)
    )
    created_at: datetime = Field(default_factory=datetime.now)
    
    def update(self, **kwargs: Any) -> "UserModel":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"O atributo '{key}' não existe na classe UserModel.")
        return self
