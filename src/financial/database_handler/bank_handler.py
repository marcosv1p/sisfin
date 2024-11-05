from uuid import UUID
from typing import List, Optional
from datetime import datetime

from infra import BankRepository
from src.financial.bank import BankModel


class BankDatabaseHandler:
    _db = BankRepository()
    
    @classmethod
    def insert(cls, bank: BankModel) -> None:
        """Insere um novo banco no banco de dados."""
        result = cls._db.select_from_id(bank.bank_id.hex)
        if result:
            cls._db.delete(bank_id=bank.bank_id.hex)
        cls._db.insert(
            bank_id=bank.bank_id.hex,
            name=bank.name,
            description=bank.description,
            created_at=bank.created_at,
            url_image=bank.url_image,
        )
    
    @classmethod
    def update(cls, bank_id: UUID, bank: BankModel) -> BankModel:
        """Atualiza os dados de um banco existente."""
        cls._db.update(
            bank_id=bank.bank_id.hex,
            new_bank_id=bank.bank_id.hex if bank.bank_id != bank_id else None,
            new_name=bank.name,
            new_description=bank.description,
            new_created_at=bank.created_at,
            new_url_image=bank.url_image
        )
    
    @classmethod
    def delete(cls, bank_id: UUID) -> None:
        """Deleta um banco com base no ID fornecido."""
        cls._db.delete(bank_id.hex)
    
    @classmethod
    def get(cls, bank_id: UUID) -> Optional[BankModel]:
        """Obtém um banco pelo ID."""
        raw_data = cls._db.select_from_id(bank_id.hex)
        if raw_data:
            data = raw_data.to_dict()
            data.update(
                bank_id=bank_id,
                created_at=datetime.fromisoformat(data.get("created_at"))
                )
            return BankModel(**data)
        return None
    
    @classmethod
    def get_all(cls) -> List[BankModel]:
        """Obtém todos os bancos."""
        raw_data = cls._db.select()
        if raw_data:
            data = []
            for bank in raw_data:
                d = bank.to_dict()
                d.update(
                    bank_id=UUID(d.get("bank_id")),
                    created_at=datetime.fromisoformat(d.get("created_at"))
                )
                data.append(BankModel(**d))
            return data
        return []
