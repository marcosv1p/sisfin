from uuid import UUID
from typing import List, Optional

from infra import TransactionCategoryRepository
from src.financial.models import TransactionCategoryModel
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.database_adapter_errors import transaction_category_db_adapter_error


class TransactionCategoryDatabaseAdapter(DatabaseAdapterInterface):
    _db = TransactionCategoryRepository()
    
    @classmethod
    def insert(cls, transaction_category: TransactionCategoryModel) -> None:
        # Valida o tipo do argumento 'transaction_category'
        if not isinstance(transaction_category, TransactionCategoryModel):
            raise transaction_category_db_adapter_error.UnexpectedArgumentTypeError()
        
        exist_transaction_category = cls._db.select_from_id(transaction_category.id.hex)
        
        # Valida se a conta já existe
        if exist_transaction_category:
            raise transaction_category_db_adapter_error.TransactionCategoryAlreadyExistsError()
        
        result = cls._db.insert(
            id=transaction_category.id.hex,
            name=transaction_category.name,
            created_at=transaction_category.created_at,
            user_id=transaction_category.user_id.hex,
        )
        
        return result is not None
    
    @classmethod
    def update(cls, id: UUID, transaction_category: TransactionCategoryModel) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_db_adapter_error.UnexpectedArgumentTypeError()
        
        # Valida o tipo do argumento 'transaction_category'
        if not isinstance(transaction_category, TransactionCategoryModel):
            raise transaction_category_db_adapter_error.UnexpectedArgumentTypeError()
        
        current_transaction_category = cls._db.select_from_id(id=id.hex)
        
        # Valida se a conta existe
        if current_transaction_category is None:
            raise transaction_category_db_adapter_error.TransactionCategoryNotFoundError()
        
        # Valida se o 'id' foi modificado
        if transaction_category.id and transaction_category.id != UUID(current_transaction_category.id):
            raise transaction_category_db_adapter_error.TransactionCategoryDBAdapterError("Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'transaction_category'")
        
        # Aqui cria um mapa de atualizações com o novo valor e o valor atual
        updates_map = {
            "name": {"new_value": transaction_category.name, "current_value": current_transaction_category.name},
            "created_at": {"new_value": transaction_category.created_at, "current_value": current_transaction_category.created_at},
            "user_id": {"new_value": transaction_category.user_id.hex, "current_value": current_transaction_category.user_id},
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
                raise transaction_category_db_adapter_error.TransactionCategoryDBAdapterError("Falha ao tentar atualizar 'TransactionCategory'")
    
    @classmethod
    def delete(cls, id: UUID) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_db_adapter_error.UnexpectedArgumentTypeError()
        cls._db.delete(id=id.hex)
    
    @classmethod
    def get(cls, id: UUID) -> Optional[TransactionCategoryModel]:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_category_db_adapter_error.UnexpectedArgumentTypeError()
        
        data = cls._db.select_from_id(id=id.hex)
        
        if data:
            return TransactionCategoryModel(
                id=UUID(data.id),
                name=data.name,
                created_at=data.created_at,
                user_id=UUID(data.user_id),
            )
        return None
    
    @classmethod
    def get_all(cls) -> List[TransactionCategoryModel]:
        data = cls._db.select()
        if data:
            result = []
            for transaction_category in data:
                result.append(
                    TransactionCategoryModel(
                        id=UUID(transaction_category.id),
                        name=transaction_category.name,
                        created_at=transaction_category.created_at,
                        user_id=UUID(transaction_category.user_id),
                    )
                )
            return result
        return []
