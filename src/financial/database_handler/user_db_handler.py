from uuid import UUID
from typing import List, Optional

from infra import UserRepository
from src.financial.models import UserModel
from src.financial.exceptions.database_handler_error import UserDatabaseHandlerError
from src.financial.database_handler.database_handler_interface import DatabaseHandlerInterface


class UserDatabaseHandler(DatabaseHandlerInterface):
    _db = UserRepository()
    
    @classmethod
    def insert(cls, user: UserModel) -> None:
        exist_user = cls._db.select_from_id(user.user_id.hex)
        if exist_user:
            raise UserDatabaseHandlerError("Já existe um 'User' com mesmo 'user_id' no banco de dados")
        cls._db.insert(
            user_id=user.user_id.hex,
            nickname=user.nickname,
            created_at=user.created_at,
        )
    
    @classmethod
    def update(cls, user_id: UUID, user: UserModel) -> None:
        current_user = cls._db.select_from_id(user_id=user_id.hex)
        
        if not current_user:
            raise UserDatabaseHandlerError("User não encontrado.")
        
        if user.user_id and user.user_id != UUID(current_user.user_id):
            raise UserDatabaseHandlerError("Incosistencia entre o parametro 'user_id' e a proprienda user_id do paramentro 'user'")
        
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
                user_id=user_id.hex,
                name=updates.get("nickname"),
                created_at=updates.get("new_created_at"),
            )
            if not result:
                raise UserDatabaseHandlerError("Falha ao tentar atualizar 'User'")
    
    @classmethod
    def delete(cls, user_id: UUID) -> None:
        cls._db.delete(user_id.hex)
    
    @classmethod
    def get(cls, user_id: UUID) -> Optional[UserModel]:
        data = cls._db.select_from_id(user_id.hex)
        if data:
            return UserModel(
                user_id=UUID(data.user_id),
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
                        user_id=UUID(user.user_id),
                        nickname=user.nickname,
                        created_at=user.created_at,
                    )
                )
            return result
        return []
