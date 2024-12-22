from uuid import UUID, uuid4
from datetime import datetime
from pydantic import Field, BaseModel


class AccountTagModel(BaseModel):
    # UUID da tag
    id: UUID = Field(default_factory=uuid4)
    
    # Nome da tag
    name: str
    
    # Data de criação da tag
    created_at: datetime = Field(default_factory=datetime.now)
    
    # UUID do usuario que criou que pertense a tag
    user_id: UUID
    
    def get_current_dict_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "user_id": self.user_id
        }