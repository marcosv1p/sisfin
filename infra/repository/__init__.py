from infra.repository.bank_repository import BankRepository
from infra.repository.bank_account_repository import BankAccountRepository
from infra.repository.transaction_repository import TransactionRepository

from infra.configs import DBConnectionHandler, Base


with DBConnectionHandler() as db:
    engine = db.get_engine()
    Base.metadata.create_all(engine)