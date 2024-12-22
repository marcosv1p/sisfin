from uuid import UUID
from typing import List, Optional
from decimal import Decimal

from infra.repository import TransactionRepository
from src.financial.models import TransactionModel, TransactionTypes
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.database_adapter_errors import transaction_db_adapter_error


class TransactionDatabaseAdapter(DatabaseAdapterInterface):
    _db = TransactionRepository()
    
    @classmethod
    def insert(cls, transaction: TransactionModel) -> None:
        # Valida o tipo do argumento 'transaction'
        if not isinstance(transaction, TransactionModel):
            raise transaction_db_adapter_error.UnexpectedArgumentTypeError()
        
        exist_trasaction = cls._db.select_from_id(transaction.id.hex)
        
        # Valida se a transação já existe
        if exist_trasaction:
            raise transaction_db_adapter_error.TransactionAlreadyExistsError()
        
        result = cls._db.insert(
            id=transaction.id.hex,
            date=transaction.date,
            description=transaction.description,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type.value,
            paid=transaction.paid,
            ignore=transaction.ignore,
            visible=transaction.visible,
            category_id=transaction.category_id.hex,
            tag_id=transaction.tag_id.hex,
            account_id_origin=transaction.account_id_origin.hex,
            account_id_destination=transaction.account_id_destination.hex,
            created_at=transaction.created_at,
            user_id=transaction.user_id.hex,
        )
        
        return result is not None
    
    @classmethod
    def update(cls, id: UUID, transaction: TransactionModel) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_db_adapter_error.UnexpectedArgumentTypeError()
        
        # Valida o tipo do argumento 'transaction'
        if not isinstance(transaction, TransactionModel):
            raise transaction_db_adapter_error.UnexpectedArgumentTypeError()
        
        current_transaction = cls._db.select_from_id(id=id.hex)
        
        # Valida se existe um usuário com o id informado
        if current_transaction is None:
            raise transaction_db_adapter_error.TransactionNotFoundError()
        
        # Valida se o 'id' foi modificado
        if transaction.id and transaction.id != UUID(current_transaction.id):
            raise transaction_db_adapter_error.TransactionDBAdapterError(error_message="Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'transaction'")
        
        updates_map = {
            "date": {"new_value": transaction.date, "current_value": current_transaction.date},
            "description": {"new_value": transaction.description, "current_value":current_transaction.description},
            "amount": {"new_value": transaction.amount, "current_value":current_transaction.amount},
            "transaction_type": {"new_value": transaction.transaction_type.value, "current_value": current_transaction.transaction_type},
            "paid": {"new_value": transaction.paid, "current_value":current_transaction.paid},
            "ignore": {"new_value": transaction.ignore, "current_value":current_transaction.ignore},
            "visible": {"new_value": transaction.visible, "current_value":current_transaction.visible},
            "category_id": {"new_value": transaction.category_id.hex, "current_value":current_transaction.category_id},
            "tag_id": {"new_value": transaction.tag_id.hex, "current_value":current_transaction.tag_id},
            "account_id_origin": {"new_value": getattr(transaction.account_id_origin, "hex", None), "current_value":current_transaction.account_id_origin},
            "account_id_destination": {"new_value": transaction.account_id_destination.hex, "current_value":current_transaction.account_id_destination},
            "created_at": {"new_value": transaction.created_at, "current_value":current_transaction.created_at},
            "user_id": {"new_value": transaction.user_id.hex, "current_value":current_transaction.user_id},
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
                raise transaction_db_adapter_error.TransactionDBAdapterError("Falha ao tentar atualizar 'Transaction'")
    
    @classmethod
    def delete(cls, id: UUID) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_db_adapter_error.UnexpectedArgumentTypeError()
        cls._db.delete(id=id.hex)
    
    @classmethod
    def get(cls, id: UUID) -> Optional[TransactionModel]:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise transaction_db_adapter_error.UnexpectedArgumentTypeError()
        data = cls._db.select_from_id(id=id.hex)
        if not data:
            return None
        return TransactionModel(
            id=UUID(data.id),
            date=data.date,
            description=data.description,
            amount=Decimal(data.amount),
            transaction_type=TransactionTypes(data.transaction_type),
            paid=data.paid,
            ignore=data.ignore,
            visible=data.visible,
            category_id=UUID(data.category_id),
            tag_id=UUID(data.tag_id),
            account_id_origin=UUID(data.account_id_origin),
            account_id_destination=UUID(data.account_id_destination),
            created_at=data.created_at,
            user_id=UUID(data.user_id),
        )
    
    @classmethod
    def get_all(cls) -> List[TransactionModel]:
        data = cls._db.select()
        if data:
            result = []
            for transaction in data:
                result.append(
                    TransactionModel(
                        id=UUID(transaction.id),
                        date=transaction.date,
                        description=transaction.description,
                        amount=Decimal(transaction.amount),
                        transaction_type=TransactionTypes(transaction.transaction_type),
                        paid=transaction.paid,
                        ignore=transaction.ignore,
                        visible=transaction.visible,
                        category_id=UUID(transaction.category_id),
                        tag_id=UUID(transaction.tag_id),
                        account_id_origin=UUID(transaction.account_id_origin),
                        account_id_destination=UUID(transaction.account_id_destination),
                        created_at=transaction.created_at,
                        user_id=UUID(transaction.user_id),
                    )
                )
            return result
        return []

