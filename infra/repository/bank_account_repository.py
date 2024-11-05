from datetime import datetime
from sqlalchemy.orm import joinedload

from infra.entities.bank import Bank
from infra.entities.bank_account import BankAccount
from infra.configs.connection import DBConnectionHandler


class BankAccountRepository:
    def __init__(self):
        self.db = DBConnectionHandler()
    
    def select(self):
        """Consulta todas as contas bancárias no banco de dados.
        
        Retorna uma lista de tuplas contendo o ID da conta, nome e saldo.
        """
        with self.db as db:
            data = db.session\
                .query(BankAccount)\
                .options(joinedload(BankAccount.bank))\
                .all()
        return data
    
    def select_from_id(self, account_id: str) -> BankAccount:
        """Consulta uma conta bancária pelo ID fornecido.
        
        Args:
            id (str): O ID da conta bancária.

        Retorna:
            BankAccount: A conta bancária correspondente ao ID, ou None se não encontrada.
        """
        with self.db as db:
            return db.session.query(BankAccount).filter(BankAccount.account_id == account_id).one_or_none()
    
    def insert(self, account_id: str, name: str, description: str, created_at: datetime, bank_id: str, balance: float) -> str:
        """Insere uma nova conta bancária no banco de dados.
        
        Args:
            account_id (str): O ID da conta.
            name (str): O nome da conta.
            description (str): A descrição da conta.
            created_at (datetime): A data de criação da conta.
            bank (Bank): O objeto Bank associado à conta.
            balance (float): O saldo inicial da conta.

        Retorna:
            str: O ID da conta recém-criada.
        """
        with self.db as db:
            new_account = BankAccount(
                account_id=account_id,
                name=name,
                description=description,
                balance=balance,
                bank_id=bank_id,
                created_at=created_at
            )
            db.session.add(new_account)
            db.session.commit()
            return new_account.account_id

    def delete(self, account_id: str):
        """Deleta uma conta bancária com base no ID fornecido.
        
        Args:
            account_id (str): O ID da conta a ser deletada.
        """
        with self.db as db:
            db.session.query(BankAccount).filter(BankAccount.account_id == account_id).delete()
            db.session.commit()

    def update(self, account_id: str, new_account_id: str = None, new_name: str = None, new_description: str = None, new_created_at: datetime = None, new_bank_id: str = None, new_balance: float = None):
        """Atualiza uma conta bancária com base no ID fornecido.
        
        Args:
            account_id (str): O ID da conta a ser atualizada.
            new_account_id (str, optional): O novo ID da conta. Defaults to None.
            new_name (str, optional): O novo nome da conta. Defaults to None.
            new_description (str, optional): A nova descrição da conta. Defaults to None.
            new_created_at (datetime, optional): A nova data de criação da conta. Defaults to None.
            new_bank (Bank, optional): O novo banco associado à conta. Defaults to None.
            new_balance (float, optional): O novo saldo da conta. Defaults to None.

        Retorna:
            BankAccount: A conta bancária atualizada, ou None se a conta não foi encontrada.
        """
        with self.db as db:
            account = db.session.query(BankAccount).filter(BankAccount.account_id == account_id).first()
            if account:
                if new_name:
                    account.name = new_name
                if new_description:
                    account.description = new_description
                if new_balance is not None:
                    account.balance = new_balance
                if new_bank_id:
                    account.bank_id = new_bank_id
                if new_created_at:
                    account.created_at = new_created_at
                if new_account_id:
                    new_account = BankAccount(
                        account_id=new_account_id,
                        name=account.name,
                        description=account.description,
                        balance=account.balance,
                        bank_id=account.bank_id,
                        created_at=account.created_at
                    )
                    account_id = new_account_id
                    db.session.delete(account)
                    db.session.add(new_account)
                db.session.commit()
                return self.select_from_id(account_id=account_id)
            return None
