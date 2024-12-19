from uuid import UUID, uuid4
from datetime import datetime
from pydantic import Field, BaseModel


class UserModel(BaseModel):
    # UUID do usuário
    id: UUID = Field(default_factory=uuid4)
    
    # Apelido do usuário
    nickname: str
    
    # Data de criação do usuário
    created_at: datetime = Field(default_factory=datetime.now)
    
    def update(self, **kwargs) -> "UserModel":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"O atributo '{key}' não existe na classe UserModel.")
        return self
    
    def get_current_dict_data(self) -> dict:
        return {
            "id": self.id.hex,
            "nickname": self.nickname,
            "created_at": self.created_at,
        }
