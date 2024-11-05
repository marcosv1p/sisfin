import re
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, PrivateAttr, Field, AnyUrl, constr
from typing import Any, Optional


class BankModel(BaseModel):
    name: constr(min_length=1, max_length=64, pattern=re.compile(r"^[\w\s\-\.:çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)) = Field(default_factory=lambda: uuid4().hex)
    description: constr(max_length=255, pattern=re.compile(r"^[\w\s\-\.:çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)) = Field(default=None)
    url_image: Optional[AnyUrl] = Field(default=None)
    
    bank_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    
    def update(self, **kwargs: Any) -> "BankModel":
        updated_data = self.model_dump()
        updated_data.update(kwargs)
        return BankModel(**updated_data)
