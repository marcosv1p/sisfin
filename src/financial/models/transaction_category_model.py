from uuid import UUID, uuid4
from datetime import datetime
from pydantic import Field, BaseModel


class TransactionCategoryModel(BaseModel):
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