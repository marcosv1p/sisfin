from uuid import UUID
from typing import List, Optional

from infra import UserRepository
from src.financial.models import UserModel
from src.financial.interfaces.database_interfaces import DatabaseAdapterInterface
from src.financial.exceptions.database_adapter_errors import UserDBAdapterError, UserNotFoundError, UserAlreadyExistsError, UnexpectedArgumentTypeError


class UserDatabaseAdapter(DatabaseAdapterInterface):
    _db = UserRepository()
    
    @classmethod
    def insert(cls, user: UserModel) -> None:
        if not isinstance(user, UserModel):
            raise UnexpectedArgumentTypeError()
        
        exist_user = cls._db.select_from_id(user.id.hex)
        
        if exist_user:
            raise UserAlreadyExistsError()
        
        result = cls._db.insert(
            id=user.id.hex,
            nickname=user.nickname,
            created_at=user.created_at,
        )
        
        return result is not None
    
    @classmethod
    def update(cls, id: UUID, user: UserModel) -> None:
        if isinstance(user, UserModel):
            raise UnexpectedArgumentTypeError()
        
        if isinstance(id, UUID):
            raise UnexpectedArgumentTypeError()
        
        current_user = cls._db.select_from_id(id=id.hex)
        
        if not current_user:
            raise UserNotFoundError()
        
        if user.id and user.id != UUID(current_user.id):
            error = UserDBAdapterError()
            error.error_message = "Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'user'"
            raise error
        
        updates = {}
        
        check = {
            "nickname": {"new_value":user.nickname, "comparator":current_user.nickname},
            "created_at": {"new_value":user.created_at, "comparator":current_user.created_at},
        }
        
        for key, value in check.items():
            if value["new_value"] is not None and value["new_value"] != value["comparator"]:
                updates[key] = value["new_value"]
        
        if updates:
            result = cls._db.update(
                id=id.hex,
                name=updates.get("nickname"),
                created_at=updates.get("new_created_at"),
            )
            if not result:
                error = UserDBAdapterError()
                error.error_message = "Falha ao tentar atualizar 'User'"
                raise error
    
    @classmethod
    def delete(cls, id: UUID) -> None:
        cls._db.delete(id.hex)
    
    @classmethod
    def get(cls, id: UUID) -> Optional[UserModel]:
        data = cls._db.select_from_id(id.hex)
        if data:
            return UserModel(
                id=UUID(data.id),
                nickname=data.nickname,
                created_at=data.created_at,
            )
        return None
    
    @classmethod
    def get_all(cls) -> List[UserModel]:
        data = cls._db.select()
        if data:
            result = []
            for user in data:
                result.append(
                    UserModel(
                        id=UUID(user.id),
                        nickname=user.nickname,
                        created_at=user.created_at,
                    )
                )
            return result
        return []
