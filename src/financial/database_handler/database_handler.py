from src.financial.database_handler import BankDatabaseHandler, AccountDatabaseHandler, TransactionDatabaseHandler

class DatabaseHandler:
    db_bank = BankDatabaseHandler
    db_account = AccountDatabaseHandler
    db_transaction = TransactionDatabaseHandler
