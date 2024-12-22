from uuid import UUID
from typing import List, Optional

from infra import UserRepository
from src.financial.models import UserModel
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.database_adapter_errors import user_db_adapter_error


class UserDatabaseAdapter(DatabaseAdapterInterface):
    _db = UserRepository()
    
    @classmethod
    def insert(cls, user: UserModel) -> None:
        if not isinstance(user, UserModel):
            raise user_db_adapter_error.UnexpectedArgumentTypeError()
        
        exist_user = cls._db.select_from_id(user.id.hex)
        
        if exist_user:
            raise user_db_adapter_error.UserAlreadyExistsError()
        
        result = cls._db.insert(
            id=user.id.hex,
            nickname=user.nickname,
            created_at=user.created_at,
        )
        
        return result is not None
    
    @classmethod
    def update(cls, id: UUID, user: UserModel) -> None:
        # Valida o tipo do argumento 'user'
        if not isinstance(user, UserModel):
            raise user_db_adapter_error.UnexpectedArgumentTypeError()
        
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise user_db_adapter_error.UnexpectedArgumentTypeError()
        
        current_user = cls._db.select_from_id(id=id.hex)
        
        # Valida se existe um usuário com o id informado
        if current_user is None:
            raise user_db_adapter_error.UserNotFoundError()
        
        # Valida se o 'id' foi modificado
        if user.id and user.id != UUID(current_user.id):
            raise user_db_adapter_error.UserDBAdapterError(error_message="Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'user'")
        
        # Aqui cria um mapa de atualizações com o novo valor e o valor atual
        updates_map = {
            "nickname": {"new_value": user.nickname, "current_value": current_user.nickname},
            "created_at": {"new_value": user.created_at, "current_value": current_user.created_at},
        }
        
        # Aqui cria um dicionário com as atualizações que serão feitas
        updates_to_apply = {
            key: value["new_value"]
            if value["new_value"] != value["current_value"]
            else None # Isso aqui é necessario pois pode haver necidade de fornecer o argumento mesmo que vazio
            for key, value in updates_map.items()
        }
        
        if updates_to_apply:
            result = cls._db.update(id=id.hex, **updates_to_apply)
            if not result:
                raise user_db_adapter_error.UserDBAdapterError("Falha ao tentar atualizar 'User'")
    
    @classmethod
    def delete(cls, id: UUID) -> None:
        if not isinstance(id, UUID):
            raise user_db_adapter_error.UnexpectedArgumentTypeError()
        cls._db.delete(id.hex)
    
    @classmethod
    def get(cls, id: UUID) -> Optional[UserModel]:
        if not isinstance(id, UUID):
            raise user_db_adapter_error.UnexpectedArgumentTypeError()
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
