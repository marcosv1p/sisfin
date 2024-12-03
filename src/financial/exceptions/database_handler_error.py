
class DatabaseHandlerError(Exception):
    pass

class UserDatabaseHandlerError(DatabaseHandlerError):
    pass

class TransactionDatabaseHandlerError(DatabaseHandlerError):
    pass

class AccountDatabaseHandlerError(DatabaseHandlerError):
    pass
