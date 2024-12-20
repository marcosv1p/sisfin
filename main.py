from src.financial.system.financial_handler import FinancialHandler
from src.financial.models import UserModel, AccountModel, TransactionModel, TransactionsTypes
from decimal import Decimal

user01 = UserModel(nickname="Marcos")

acc01 = AccountModel(name="Acc01", description="TesteXX", created_by=user01.user_id) # 130
acc02 = AccountModel(name="Acc02", description="Teste02", created_by=user01.user_id) # 40
acc03 = AccountModel(name="Acc03", description="Teste03", created_by=user01.user_id) # 70

trasaction01 = TransactionModel(description="Add 100 01", amount=100, transaction_type=TransactionsTypes.DEPOSIT, destination=acc01.account_id, created_by=user01.user_id)
trasaction02 = TransactionModel(description="Add 100 02", amount=100, transaction_type=TransactionsTypes.DEPOSIT, destination=acc02.account_id, created_by=user01.user_id)
trasaction03 = TransactionModel(description="Add 100 03", amount=100, transaction_type=TransactionsTypes.DEPOSIT, destination=acc03.account_id, created_by=user01.user_id)
trasaction04 = TransactionModel(description="Rem 10 01", amount=10, transaction_type=TransactionsTypes.WITHDRAW, destination=acc01.account_id, created_by=user01.user_id)
trasaction05 = TransactionModel(description="Rem 20 02", amount=20, transaction_type=TransactionsTypes.WITHDRAW, destination=acc02.account_id, created_by=user01.user_id)
trasaction06 = TransactionModel(description="Rem 30 03", amount=30, transaction_type=TransactionsTypes.WITHDRAW, destination=acc03.account_id, created_by=user01.user_id)
trasaction07 = TransactionModel(description="Trf 40 02 01", amount=40, transaction_type=TransactionsTypes.TRANSFER, destination=acc01.account_id, origin=acc02.account_id, created_by=user01.user_id)

fh = FinancialHandler()

fh.add_user(user01)

fh.add_account(acc01)
fh.add_account(acc02)
fh.add_account(acc03)

fh.add_transaction(trasaction01)
fh.add_transaction(trasaction02)
fh.add_transaction(trasaction03)
fh.add_transaction(trasaction04)
fh.add_transaction(trasaction05)
fh.add_transaction(trasaction06)
fh.add_transaction(trasaction07)

for trs in fh.get_all_transactions():
    fh._execute_transaction(trs.transaction_id)





