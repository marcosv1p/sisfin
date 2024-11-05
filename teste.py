from src.financial.system.financial_handler import FinancialHandler
from src.financial.account import AccountModel
from src.financial.bank import BankModel
from src.financial.transaction import TransactionModel, TransactionsTypes

from decimal import Decimal
from uuid import UUID

fh = FinancialHandler()

# account01 = fh.get_account(UUID("5d2e447b80fe4806a8c802809c1f84aa"))
# account02 = fh.get_account(UUID("1568a22edc8140a28d40366ed09c6b5c"))
# account03 = fh.get_account(UUID("b2662ae42876469c87cefe97aa063412"))

bank01 = BankModel(name="Infinite Pay", description="Teste: bank01")
bank02 = BankModel(name="Sicoob", description="Teste: bank02")
bank03 = BankModel(name="Mercado Pago", description="Teste: bank03")

account01 = AccountModel(bank=bank01.bank_id, name="Conta reserva", description="Teste: account01") #1000
account02 = AccountModel(bank=bank02.bank_id, name="Conta para teste", description="Teste: account02") #3000
account03 = AccountModel(bank=bank03.bank_id, name="Conta para estudos", description="Teste: account03") #1500

transcation01 = TransactionModel(description="Depósito de 1000 a conta 01", value=Decimal("1000.00"), destination=account01, transaction_type=TransactionsTypes.DEPOSIT)
transcation02 = TransactionModel(description="Saque de 500 a conta 01", value=Decimal("500.00"), destination=account01, transaction_type=TransactionsTypes.WITHDRAW)
transcation03 = TransactionModel(description="Depósito de 5000 a conta 02", value=Decimal("5000.00"), destination=account02, transaction_type=TransactionsTypes.DEPOSIT)
transcation04 = TransactionModel(description="Transferência de 1500 da conta 02 para conta 03", value=Decimal("1500.00"), destination=account03, origin=account02, transaction_type=TransactionsTypes.TRANSFER)
transcation05 = TransactionModel(description="Transferência de 500 da conta 02 para conta 01", value=Decimal("500.00"), destination=account01, origin=account02, transaction_type=TransactionsTypes.TRANSFER)

fh.add_bank(bank=bank01)
fh.add_bank(bank=bank02)
fh.add_bank(bank=bank03)

fh.add_account(account=account01)
fh.add_account(account=account02)
fh.add_account(account=account03)

fh.add_transaction(transaction=transcation01)
fh.add_transaction(transaction=transcation02)
fh.add_transaction(transaction=transcation03)
fh.add_transaction(transaction=transcation04)
fh.add_transaction(transaction=transcation05)



# print(".,"*30)
# for x in fh.accounts:
#     print("="*30)
#     # print(x.account_id)
#     print(x.name)
#     print(x.balance)

import time
for x in fh.transactions:

    if x.status:
        fh._undo_execute_transaction(x.transaction_id)
    else:
        fh._execute_transaction(x.transaction_id)
    for a in fh.accounts:
        if a.account_id == x.destination.account_id or a.account_id == (x.origin.account_id if x.origin else None):
            print("="*30)
            # print(x.account_id)
            print(a.description)
            print(a.balance)
            print(x.value)
            print(x.description)
    print()
    print()
    print()
    # print(x.status)
    # print()
    # fh.remove_transaction(x.transaction_id)
    # if x.destination.account_id == account02.account_id:
    #     print("+"*20)
    #     print(f"Descrição: {x.description}")
    #     print(f"Valor: {x.value}")
    #     print(f"Data: {x.date}")
    #     print(f"Conta: {x.destination.name}")
    #     print(f"Saldo: {x.destination.balance}")
    #     print(f"ID: {x.transaction_id}")
    #     print(f"Tipo: {x.transaction_type}")
    #     print(f"Situação: {x.status}")
    #     print("+"*2)
    #     print("")
    #     print("")


print(".,"*30)
fh.load_all_data()
for x in fh.accounts:
    print("="*30)
    print(F"Banco: {fh.get_bank(x.bank).name}")
    print(f"Banco ID: {fh.get_bank(x.bank).bank_id}")
    print(f"Conta: {x.name}")
    print(f"Saldo: {x.balance}")








