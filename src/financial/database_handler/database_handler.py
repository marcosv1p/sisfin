from src.financial.database_handler import UserDatabaseHandler, AccountDatabaseHandler, TransactionDatabaseHandler

class DatabaseHandler:
    handler_user = UserDatabaseHandler
    handler_account = AccountDatabaseHandler
    handler_transaction = TransactionDatabaseHandler
