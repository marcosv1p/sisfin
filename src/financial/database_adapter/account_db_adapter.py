from uuid import UUID
from decimal import Decimal
from typing import List, Optional

from infra import AccountRepository
from src.financial.models import AccountModel
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.database_adapter_errors.account_db_adapter_error import AccountDBAdapterError, AccountAlreadyExistsError, AccountNotFoundError, UnexpectedArgumentTypeError


class AccountDatabaseAdapter(DatabaseAdapterInterface):
    _db = AccountRepository()
    
    @classmethod
    def insert(cls, account: AccountModel) -> None:
        # Valida o tipo do argumento 'account'
        if not isinstance(account, AccountModel):
            raise UnexpectedArgumentTypeError()
        
        exist_account = cls._db.select_from_id(account.id.hex)
        
        # Valida se a conta já existe
        if exist_account:
            raise AccountAlreadyExistsError()
        
        result = cls._db.insert(
            id=account.id.hex,
            name=account.name,
            description=account.description,
            tag_id=getattr(account.tag_id, 'hex', account.tag_id),
            balance=account.balance,
            created_at=account.created_at,
            user_id=account.user_id.hex,
        )
        
        return result is not None
    
    @classmethod
    def update(cls, id: UUID, account: AccountModel) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise UnexpectedArgumentTypeError()
        
        # Valida o tipo do argumento 'account'
        if not isinstance(account, AccountModel):
            raise UnexpectedArgumentTypeError()
        
        current_account = cls._db.select_from_id(id=id.hex)
        
        # Valida se a conta existe
        if current_account is None:
            raise AccountNotFoundError()
        
        # Valida se o 'id' foi modificado
        if account.id and account.id != UUID(current_account.id):
            raise AccountDBAdapterError("Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'account'")
        
        # Aqui cria um mapa de atualizações com o novo valor e o valor atual
        updates_map = {
            "name": {"new_value": account.name, "current_value": current_account.name},
            "description": {"new_value": account.description, "current_value": current_account.description},
            "tag_id": {"new_value": account.tag_id.hex, "current_value": current_account.tag_id},
            "balance": {"new_value": account.balance, "current_value": current_account.balance},
            "created_at": {"new_value": account.created_at, "current_value": current_account.created_at},
            "user_id": {"new_value": account.user_id.hex, "current_value": current_account.user_id},
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
                raise AccountDBAdapterError("Falha ao tentar atualizar 'Account'")
    
    @classmethod
    def delete(cls, id: UUID) -> None:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise UnexpectedArgumentTypeError()
        cls._db.delete(id=id.hex)
    
    @classmethod
    def get(cls, id: UUID) -> Optional[AccountModel]:
        # Valida o tipo do argumento 'id'
        if not isinstance(id, UUID):
            raise UnexpectedArgumentTypeError()
        
        data = cls._db.select_from_id(id=id.hex)
        
        if data:
            return AccountModel(
                id=UUID(data.id),
                name=data.name,
                description=data.description,
                tag_id=data.tag_id,
                balance=Decimal(f"{data.balance:.2f}"),
                created_at=data.created_at,
                user_id=UUID(data.user_id),
            )
        return None
    
    @classmethod
    def get_all(cls) -> List[AccountModel]:
        data = cls._db.select()
        if data:
            result = []
            for account in data:
                result.append(
                    AccountModel(
                        id=UUID(account.id),
                        name=account.name,
                        description=account.description,
                        balance=Decimal(f"{account.balance:.2f}"),
                        tag_id=account.tag_id,
                        created_at=account.created_at,
                        user_id=UUID(account.user_id),
                    )
                )
            return result
        return []
