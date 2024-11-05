import time

from json import dumps
from datetime import datetime

from infra.repository import BankRepository, BankAccountRepository, TransactionRepository


db = BankRepository()

db.insert(
    bank_id="testexx",
    name="Teste name XX",
    description="Teste description XX",
    created_at=datetime.now(),
)

db.insert(
    bank_id="teste02",
    name="Teste name 02",
    description="Teste description 02",
    created_at=datetime.now(),
)

db.insert(
    bank_id="teste03",
    name="Teste name 03",
    description="Teste description 03",
    created_at=datetime.now(),
)

db.delete("teste03")

print(db.select_from_id("testexx").to_dict())

db.update("testexx", "teste01", "Teste name 01", "Teste description 01", datetime.now(), "URL FAKE")

db.update(bank_id="teste01", new_url_image="UrlRakiQuerJogar.com")

data = db.select()

print("\n\n".join([dumps({**d.to_dict()}, indent=4) for d in data]))











print(f"\n\n{'':=^100}\n\n")

db = BankAccountRepository()

db.insert(
    account_id="testexx",
    name="Teste name XX",
    description="Teste description XX",
    balance=0,
    created_at=datetime.now(),
    bank_id="teste01"
)

db.insert(
    account_id="teste02",
    name="Teste name 02",
    description="Teste description 02",
    balance=0,
    created_at=datetime.now(),
    bank_id="teste02"
)

db.insert(
    account_id="teste03",
    name="Teste name 03",
    description="Teste description 03",
    balance=0,
    created_at=datetime.now(),
    bank_id="teste03"
)

db.delete("teste03")

print(db.select_from_id("testexx").to_dict())

db.update(account_id="testexx",
    new_account_id="teste01",
    new_name="Teste name 01",
    new_description="Teste description 01",
    new_balance=0,
    new_created_at=datetime.now(),
    new_bank_id="teste02"
)

db.update(
    account_id="teste01",
    new_balance=999.01
)

data = db.select()

print("\n\n".join([dumps({**d.to_dict()}, indent=4) for d in data]))





















print(f"\n\n{'':=^100}\n\n")

db = TransactionRepository()

db.insert(
    transaction_id="testexx",
    date=datetime.now(),
    description="Teste description XX",
    value=0,
    transaction_type="transfer",
    origin="teste01",
    destination="teste02",
    status=True,
    created_at=datetime.now(),
)

db.insert(
    transaction_id="teste02",
    date=datetime.now(),
    description="Teste description 02",
    value=0,
    transaction_type="withdraw",
    origin=None,
    destination="teste01",
    status=False,
    created_at=datetime.now(),
)

db.insert(
    transaction_id="teste03",
    date=datetime.now(),
    description="Teste description 03",
    value=0,
    transaction_type="withdraw",
    origin=None,
    destination="teste01",
    status=True,
    created_at=datetime.now(),
)

db.delete("teste03")

print(db.select_from_id("testexx").to_dict())

db.update(transaction_id="testexx",
    new_transaction_id="teste01",
    new_date=datetime.now(),
    new_description="Teste description 01",
    new_value=20000,
    new_transaction_type="withdraw",
    new_origin="teste02",
    new_destination="teste01",
    new_status=False,
    new_created_at=datetime.now(),
)

db.update(
    transaction_id="teste01",
    new_value=999.01
)

data = db.select()

print("\n\n".join([dumps({**d.to_dict()}, indent=4) for d in data]))








