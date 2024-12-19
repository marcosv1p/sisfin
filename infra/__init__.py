from infra.entities import User, Account, AccountTag, Transaction, TransactionTag, TransactionCategory
from infra.repository import UserRepository, AccountRepository, AccountTagRepository, TransactionRepository, TransactionTagRepository, TransactionCategoryRepository
from infra.configs import DBConnectionHandler, Base

# Gambiarra que garante a tabela e o banco existir mesmo quando ainda não foi criado nada (Magica hahaha)
with DBConnectionHandler() as db:
    engine = db.get_engine()
    Base.metadata.create_all(engine)
