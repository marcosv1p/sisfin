from decimal import Decimal
from src.financial.database_handler.bank_handler import BankDatabaseHandler as db_bank
from src.financial.database_handler.account_handler import AccountDatabaseHandler as db_account
from src.financial.database_handler.transaction_hanler import TransactionDatabaseHandler as db_transaction
from src.financial.account import AccountModel
from src.financial.bank import BankModel
from src.financial.transaction import TransactionModel, TransactionsTypes
from uuid import uuid4


bank01 = BankModel(name="Teste 01", description="Teste descrição 01")
bank02 = BankModel(name="Teste 02", description="Teste descrição 02")
bank03 = BankModel(name="Teste 03", description="Teste descrição 03")

db_bank.insert(bank=bank01)
db_bank.insert(bank=bank02)
db_bank.insert(bank=bank03)

db_bank.delete(bank_id=bank03.bank_id)

print(db_bank.get(bank_id=bank02.bank_id))

print("+"*20)

print(db_bank.get_all())

print("="*100)

account01 = AccountModel(bank=bank01.bank_id, name="Teste 01", description="Teste descrição 01")
account02 = AccountModel(bank=bank02.bank_id, name="Teste 02", description="Teste descrição 02")
account03 = AccountModel(bank=bank02.bank_id, name="Teste 03", description="Teste descrição 03")

db_account.insert(account01)
db_account.insert(account02)
db_account.insert(account03)

db_account.delete(account03.account_id)

account03.balance = Decimal("999.01")

print(db_account.get(account_id=account01.account_id))
aid = account01.account_id
account03.account_id = uuid4()
print()
db_account.update(account_id=aid, account=account03)

print(db_account.get_all())

print()
print("="*100)
print()

transation01 = TransactionModel(description="Teste descrição 01", transaction_type=TransactionsTypes.DEPOSIT, destination=account02)
transation02 = TransactionModel(description="Teste descrição 02", transaction_type=TransactionsTypes.DEPOSIT, destination=account02)
transation03 = TransactionModel(description="Teste descrição 03", transaction_type=TransactionsTypes.DEPOSIT, origin=account01, destination=account02)

db_transaction.insert(transation01)
db_transaction.insert(transation02)
db_transaction.insert(transation03)

db_transaction.delete(transation03.transaction_id)

tid = transation02.transaction_id

transation02.transaction_id = uuid4()
transation02.origin = account02
transation02.description = "Teste descrição 02 MOD"

print(db_transaction.get(tid))

print()

db_transaction.update(transaction_id=tid, transaction=transation02)

print(db_transaction.get_all())











