from uuid import UUID
from typing import List, Optional

from infra import TransactionTagRepository
from src.financial.models import TransactionTagModel
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.database_adapter_errors import transaction_tag_db_adapter_error


class TransactionTagDatabaseAdapter(DatabaseAdapterInterface):
    _db = TransactionTagRepository()
    
    @classmethod
    def insert(cls, transaction_tag: TransactionTagModel) -> None:
        # Valida o tipo do argumento 'transaction_tag'
        if not isinstance(transaction_tag, TransactionTagModel):
            raise transaction_tag_db_adapter_error.UnexpectedArgumentTypeError()
        
        exist_transaction_tag = cls._db.select_from_id(transaction_tag.id.hex)
        
        # Valida se a conta já existe
        if exist_transaction_tag:
            raise transaction_tag_db_adapter_error.TransactionTagAlreadyExistsError()
        
        result = cls._db.insert(
            id=transaction_tag.id.hex,
            name=transaction_tag.name,
            created_at=transaction_tag.created_at,
            user_id=transaction_tag.user_id.hex,
        )
        
        return result is not None
    
    @classmethod
    def update(cls, id: UUID, transaction_tag: TransactionTagModel) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_tag_db_adapter_error.UnexpectedArgumentTypeError()
        
        # Valida o tipo do argumento 'transaction_tag'
        if not isinstance(transaction_tag, TransactionTagModel):
            raise transaction_tag_db_adapter_error.UnexpectedArgumentTypeError()
        
        current_transaction_tag = cls._db.select_from_id(id=id.hex)
        
        # Valida se a conta existe
        if current_transaction_tag is None:
            raise transaction_tag_db_adapter_error.TransactionTagNotFoundError()
        
        # Valida se o 'id' foi modificado
        if transaction_tag.id and transaction_tag.id != UUID(current_transaction_tag.id):
            raise transaction_tag_db_adapter_error.TransactionTagDBAdapterError("Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'transaction_tag'")
        
        # Aqui cria um mapa de atualizações com o novo valor e o valor atual
        updates_map = {
            "name": {"new_value": transaction_tag.name, "current_value": current_transaction_tag.name},
            "created_at": {"new_value": transaction_tag.created_at, "current_value": current_transaction_tag.created_at},
            "user_id": {"new_value": transaction_tag.user_id.hex, "current_value": current_transaction_tag.user_id},
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
                raise transaction_tag_db_adapter_error.TransactionTagDBAdapterError("Falha ao tentar atualizar 'TransactionTag'")
    
    @classmethod
    def delete(cls, id: UUID) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_tag_db_adapter_error.UnexpectedArgumentTypeError()
        cls._db.delete(id=id.hex)
    
    @classmethod
    def get(cls, id: UUID) -> Optional[TransactionTagModel]:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_tag_db_adapter_error.UnexpectedArgumentTypeError()
        
        data = cls._db.select_from_id(id=id.hex)
        
        if data:
            return TransactionTagModel(
                id=UUID(data.id),
                name=data.name,
                created_at=data.created_at,
                user_id=UUID(data.user_id),
            )
        return None
    
    @classmethod
    def get_all(cls) -> List[TransactionTagModel]:
        data = cls._db.select()
        if data:
            result = []
            for transaction_tag in data:
                result.append(
                    TransactionTagModel(
                        id=UUID(transaction_tag.id),
                        name=transaction_tag.name,
                        created_at=transaction_tag.created_at,
                        user_id=UUID(transaction_tag.user_id),
                    )
                )
            return result
        return []
