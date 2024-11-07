from infra.entities import Bank, BankAccount, Transaction
from infra.repository import BankRepository, BankAccountRepository, TransactionRepository
from infra.configs import DBConnectionHandler, Base

with DBConnectionHandler() as db:
    engine = db.get_engine()
    Base.metadata.create_all(engine)
