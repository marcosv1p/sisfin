
class FinancialHandlerError(Exception):
    pass

class BankAlreadyExistsError(FinancialHandlerError):
    def __init__(self, bank_id):
        super().__init__(f"O bank_id '{bank_id}' já existe no banco de dados e não pode ser adicionado novamente.")
        self.bank_id = bank_id

class BankAccountAlreadyExistsError(FinancialHandlerError):
    def __init__(self, account_id):
        super().__init__(f"A conta bancária com o ID '{account_id}' já existe no banco de dados e não pode ser adicionada novamente.")
        self.account_id = account_id

class TransactionAlreadyExistsError(FinancialHandlerError):
    def __init__(self, transaction_id):
        super().__init__(f"A transação com o ID '{transaction_id}' já existe no banco de dados e não pode ser adicionada novamente.")
        self.transaction_id = transaction_id

class BankNotFoundError(FinancialHandlerError):
    def __init__(self, bank_id):
        super().__init__(f"O banco com ID '{bank_id}' não existe no banco de dados e a operação não pode ser realizada.")
        self.bank_id = bank_id

class BankAccountNotFoundError(FinancialHandlerError):
    def __init__(self, account_id):
        super().__init__(f"A conta bancária com ID '{account_id}' não existe no banco de dados e não pode ser atualizada.")
        self.account_id = account_id

class TransactionNotFoundError(FinancialHandlerError):
    def __init__(self, transaction_id):
        super().__init__(f"A transação com ID '{transaction_id}' não existe no banco de dados e não pode ser atualizada.")
        self.transaction_id = transaction_id
