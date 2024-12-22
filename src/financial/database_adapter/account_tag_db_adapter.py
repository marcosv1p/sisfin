from uuid import UUID
from typing import List, Optional

from infra import AccountTagRepository
from src.financial.models import AccountTagModel
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.database_adapter_errors import account_tag_db_adapter_error


class AccountTagDatabaseAdapter(DatabaseAdapterInterface):
    _db = AccountTagRepository()
    
    @classmethod
    def insert(cls, account_tag: AccountTagModel) -> None:
        # Valida o tipo do argumento 'account_tag'
        if not isinstance(account_tag, AccountTagModel):
            raise account_tag_db_adapter_error.UnexpectedArgumentTypeError()
        
        exist_account_tag = cls._db.select_from_id(account_tag.id.hex)
        
        # Valida se a conta já existe
        if exist_account_tag:
            raise account_tag_db_adapter_error.AccountTagAlreadyExistsError()
        
        result = cls._db.insert(
            id=account_tag.id.hex,
            name=account_tag.name,
            created_at=account_tag.created_at,
            user_id=account_tag.user_id.hex,
        )
        
        return result is not None
    
    @classmethod
    def update(cls, id: UUID, account_tag: AccountTagModel) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_db_adapter_error.UnexpectedArgumentTypeError()
        
        # Valida o tipo do argumento 'account_tag'
        if not isinstance(account_tag, AccountTagModel):
            raise account_tag_db_adapter_error.UnexpectedArgumentTypeError()
        
        current_account_tag = cls._db.select_from_id(id=id.hex)
        
        # Valida se a conta existe
        if current_account_tag is None:
            raise account_tag_db_adapter_error.AccountTagNotFoundError("Conta não encontrada.")
        
        # Valida se o 'id' foi modificado
        if account_tag.id and account_tag.id != UUID(current_account_tag.id):
            raise account_tag_db_adapter_error.AccountTagDBAdapterError("Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'account_tag'")
        
        # Aqui cria um mapa de atualizações com o novo valor e o valor atual
        updates_map = {
            "name": {"new_value": account_tag.name, "current_value": current_account_tag.name},
            "created_at": {"new_value": account_tag.created_at, "current_value": current_account_tag.created_at},
            "user_id": {"new_value": account_tag.user_id.hex, "current_value": current_account_tag.user_id},
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
                raise account_tag_db_adapter_error.AccountTagDBAdapterError("Falha ao tentar atualizar 'AccountTag'")
    
    @classmethod
    def delete(cls, id: UUID) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_db_adapter_error.UnexpectedArgumentTypeError()
        cls._db.delete(id=id.hex)
    
    @classmethod
    def get(cls, id: UUID) -> Optional[AccountTagModel]:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise account_tag_db_adapter_error.UnexpectedArgumentTypeError()
        
        data = cls._db.select_from_id(id=id.hex)
        
        if data:
            return AccountTagModel(
                id=UUID(data.id),
                name=data.name,
                created_at=data.created_at,
                user_id=UUID(data.user_id),
            )
        return None
    
    @classmethod
    def get_all(cls) -> List[AccountTagModel]:
        data = cls._db.select()
        if data:
            result = []
            for account_tag in data:
                result.append(
                    AccountTagModel(
                        id=UUID(account_tag.id),
                        name=account_tag.name,
                        created_at=account_tag.created_at,
                        user_id=UUID(account_tag.user_id),
                    )
                )
            return result
        return []
