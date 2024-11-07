import time

from uuid import UUID
from decimal import Decimal

from src.financial.bank import BankModel
from src.financial.account import AccountModel
from src.financial.system.financial_handler import FinancialHandler
from src.financial.transaction import TransactionModel, TransactionsTypes


fh = FinancialHandler()

if data:=fh.get_all_transactions():
    for transaction in data:
        fh.remove_transaction(transaction.transaction_id)

if data:=fh.get_all_accounts():
    for account in data:
        fh.remove_account(account.account_id)

if data:=fh.get_all_banks():
    for bank in data:
        fh.remove_bank(bank.bank_id)

bank01 = BankModel(name="Infinite Pay", description="Teste: Bank01")
bank02 = BankModel(name="Sicoob", description="Teste: Bank02")
bank03 = BankModel(name="Mercado Pago", description="Teste: Bank03")

account01 = AccountModel(bank=bank01.bank_id, name="Conta reserva", description="Teste: Account01", balance=Decimal("0.00")) #1000
account02 = AccountModel(bank=bank02.bank_id, name="Conta para teste", description="Teste: Account02", balance=Decimal("0.00")) #3000
account03 = AccountModel(bank=bank03.bank_id, name="Conta para estudos", description="Teste: Account03", balance=Decimal("0.00")) #1500

transcation01 = TransactionModel(description="Depósito de 10 a conta 01", value=Decimal("10.00"), destination=account01, transaction_type=TransactionsTypes.DEPOSIT)
transcation02 = TransactionModel(description="Saque de 5 a conta 01", value=Decimal("5.00"), destination=account01, transaction_type=TransactionsTypes.WITHDRAW)
transcation03 = TransactionModel(description="Depósito de 50 a conta 02", value=Decimal("50.00"), destination=account02, transaction_type=TransactionsTypes.DEPOSIT)
transcation04 = TransactionModel(description="Transferência de 15 da conta 02 para conta 03", value=Decimal("15.00"), destination=account03, origin=account02, transaction_type=TransactionsTypes.TRANSFER)
transcation05 = TransactionModel(description="Transferência de 5 da conta 02 para conta 01", value=Decimal("5.00"), destination=account01, origin=account02, transaction_type=TransactionsTypes.TRANSFER)

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


import os
for x in fh.get_all_transactions():
    print("="*103)
    print(f"\n|{'ID':.^50}|{'DESCRIPTION':.^50}|")
    print(f"|{str(x.transaction_id): ^50}|{str(x.description): ^50}|")
    print(f"|{'':.^50}|{'':.^50}|")
    print()
    print(f"\n|{'DATE':.^50}|{'VALUE':.^50}|")
    print(f"|{str(x.date): ^50}|{str(x.value): ^50}|")
    print(f"|{'':.^50}|{'':.^50}|")
    print()
    print(f"\n|{'DESTINATION DESCRIPTION':.^50}|{'DESTINATION BALANCE':.^50}|")
    print(f"|{str(next(a.description if a.account_id == x.destination.account_id else "FAIL" for a in fh.get_all_accounts())): ^50}|{str(next(a.account_id if a.account_id == x.destination.account_id else "FAIL" for a in fh.get_all_accounts())): ^50}|")
    print(f"|{'':.^50}|{'':.^50}|")
    print()
    print(f"\n|{'ORIGIN DESCRIPTION':.^50}|{'ORIGIN BALANCE':.^50}|")
    print(f"|{str(next(a.description if a.account_id == (x.origin.account_id if x.origin else None) else None for a in fh.get_all_accounts())): ^50}|{str(next(a.balance if a.account_id == (x.origin.account_id if x.origin else None) else None for a in fh.get_all_accounts())): ^50}|")
    print(f"|{'':.^50}|{'':.^50}|")
    # fh._execute_transaction(transaction_id=x.transaction_id)
    # os.system("pause")
    fh._undo_execute_transaction(transaction_id=x.transaction_id)
    # fh._execute_transaction(transaction_id=x.transaction_id)
    # for a in fh.accounts:
    #     if a.account_id == x.destination.account_id or :
    #         print("."*50)
    #         # print(x.account_id)
    #         print(a.description)
    #         print(a.balance)
    #         print(x.value)
    #         print(x.description)
    #     elif a.account_id == (x.origin.account_id if x.origin else None):
            
    # print(".,"*30)
    # if x.status:
    #     print("_undo_execute_transaction")
    #     fh._undo_execute_transaction(x.transaction_id)
    #     pass
    # else:
    #     print("_execute_transaction")
    #     fh._execute_transaction(x.transaction_id)
    #     pass
    # for a in fh.accounts:
    #     if a.account_id == x.destination.account_id or a.account_id == (x.origin.account_id if x.origin else None):
    #         print("="*30)
    #         # print(x.account_id)
    #         print(a.description)
    #         print(a.balance)
    #         print(x.value)
    #         print(x.description)
    # print()
    # print()
    # print()
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


# print(".,"*30)
# fh.load_all_data()
# for x in fh.accounts:
#     print("="*30)
#     print(F"Banco: {fh.get_bank(x.bank).name}")
#     print(f"Banco ID: {fh.get_bank(x.bank).bank_id}")
#     print(f"Conta: {x.name}")
#     print(f"Saldo: {x.balance}")






