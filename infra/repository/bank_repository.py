from datetime import datetime
from typing import Optional, List

from infra.entities.bank import Bank
from infra.configs.connection import DBConnectionHandler


class BankRepository:
    def __init__(self) -> None:
        self.db = DBConnectionHandler()
    
    def select(self) -> List[Bank]:
        """Consulta todas as contas bancárias no banco de dados."""
        with DBConnectionHandler() as db:
            data = db.session\
                .query(Bank)\
                .all()
            return data
    
    def select_from_id(self, bank_id: str) -> Optional[Bank]:
        """Consulta todas as contas bancárias no banco de dados."""
        with DBConnectionHandler() as db:
            data = db.session\
                .query(Bank)\
                .filter(Bank.bank_id==bank_id)\
                .one_or_none()
            return data
    
    def insert(self, bank_id:str, name: str, description: str, created_at: datetime, url_image: str = None) -> Bank:
        with self.db as db:
            new_bank = Bank(
                bank_id=bank_id,
                name=name,
                description=description,
                created_at=created_at,
                url_image=url_image
            )
            db.session.add(new_bank)
            db.session.commit()
            return new_bank
    
    def delete(self, bank_id: str) -> None:
        """Deleta uma conta bancária com base no ID fornecido."""
        with DBConnectionHandler() as db:
            db.session.query(Bank).filter(Bank.bank_id == bank_id).delete()
            db.session.commit()
    
    def update(self, bank_id:str, new_bank_id:str=None, new_name: str=None, new_description: str=None, new_create_at: datetime=None, new_url_image: str=None) -> Optional[Bank]:
        """Atualiza uma conta bancária com base no ID fornecido."""
        with DBConnectionHandler() as db:
            bank = db.session.query(Bank).filter(Bank.bank_id == bank_id).first()
            if bank:
                if new_name:
                    bank.name = new_name
                if new_description is not None:
                    bank.description = new_description
                if new_create_at is not None:
                    bank.created_at = new_create_at
                if new_url_image is not None:
                    bank.url_image = new_url_image
                if new_bank_id is not None:
                    new_bank = Bank(
                        bank_id=new_bank_id,
                        name=bank.name,
                        description=bank.description,
                        created_at=bank.created_at,
                        url_image=bank.url_image
                    )
                    bank_id = new_bank_id
                    db.session.delete(bank)
                    db.session.add(new_bank)
                db.session.commit()
                return self.select_from_id(bank_id=bank_id)
            return None
