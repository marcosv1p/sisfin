from infra.entities import User, Account, Transaction
from infra.repository import UserRepository, AccountRepository, TransactionRepository
from infra.configs import DBConnectionHandler, Base

# Gambiarra que garante a tabela e o banco existir
with DBConnectionHandler() as db:
    engine = db.get_engine()
    Base.metadata.create_all(engine)
