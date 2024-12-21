import pytest
import uuid
import datetime

from decimal import Decimal
from typing import Optional, List

from infra.entities import Transaction
from src.financial.database_adapter.transaction_db_adapter import TransactionDatabaseAdapter
from src.financial.models import TransactionModel, TransactionTypes
from src.financial.exceptions.database_adapter_errors.transaction_db_adapter_error import TransactionAlreadyExistsError, TransactionDBAdapterError, TransactionNotFoundError, UnexpectedArgumentTypeError


REGISTER = []

TRASACTION_ID = uuid.uuid4()
DATE = datetime.datetime.now()
DESCRIPTION = "TESTER ACCOUNT DESCRIPTION"
AMOUNT = Decimal("100.00")
TRANSACTION_TYPE = TransactionTypes.INCOME
PAID = True
IGNORE = True
VISIBLE = True
CATEGAORY_ID = uuid.uuid4()
TAG_ID = uuid.uuid4()
ACCOUNT_ID_ORIGIN = uuid.uuid4()
ACCOUNT_ID_DESTINATION = uuid.uuid4()
CREATED_AT = datetime.datetime.now()
USER_ID = uuid.uuid4()


class MockUserRepository:
    def __init__(self) -> None:
        self.register = REGISTER
    
    def select(self) -> List[Transaction]:
        return self.register
    
    def select_from_id(self, id: str) -> Optional[Transaction]:
        return next((transaction for transaction in self.register if transaction.id == id), None)
    
    def insert(self,
            id: str,
            date: datetime.datetime,
            description: str,
            amount: float,
            transaction_type: str,
            paid: bool,
            ignore: bool,
            visible: bool,
            category_id: str,
            tag_id: str,
            account_id_origin: str,
            account_id_destination: str,
            created_at: datetime,
            user_id: str,) -> Transaction:
        new_trasaction = Transaction(
            id = id,
            date = date,
            description = description,
            amount = amount,
            transaction_type = transaction_type,
            paid = paid,
            ignore = ignore,
            visible = visible,
            category_id = category_id,
            tag_id = tag_id,
            account_id_origin = account_id_origin,
            account_id_destination = account_id_destination,
            created_at = created_at,
            user_id = user_id,
        )
        self.register.append(new_trasaction)
        return new_trasaction
    
    def update(self,
            id: str,
            date: datetime.datetime,
            description: str,
            amount: float,
            transaction_type: str,
            paid: bool,
            ignore: bool,
            visible: bool,
            category_id: str,
            tag_id: str,
            account_id_origin: str,
            account_id_destination: str,
            created_at: datetime,
            user_id: str,) -> Optional[Transaction]:
        transaction = next((transaction for transaction in self.register if transaction.id == id), None)
        idx = self.register.index(transaction)
        
        if not transaction:
            return None
        
        fields_to_update = {
            "id" : id,
            "date" : date,
            "description" : description,
            "amount" : amount,
            "transaction_type" : transaction_type,
            "paid" : paid,
            "ignore" : ignore,
            "visible" : visible,
            "category_id" : category_id,
            "tag_id" : tag_id,
            "account_id_origin" : account_id_origin,
            "account_id_destination" : account_id_destination,
            "created_at" : created_at,
            "user_id" : user_id,
        }
        
        for field, value in fields_to_update.items():
            if value is not None:
                setattr(transaction, field, value)
        self.register.pop(idx)
        self.register.insert(idx, transaction)
        return self.select_from_id(id=id)
    
    def delete(self, id: str) -> None:
        self.register.remove(next((transaction for transaction in self.register if transaction.id == id), None))


@pytest.fixture
def transaction_db_adapter():
    mocked = TransactionDatabaseAdapter
    mocked._db = MockUserRepository()
    return mocked


@pytest.fixture
def transaction_model():
    return TransactionModel(
        id = TRASACTION_ID,
        date = DATE,
        description = DESCRIPTION,
        amount = AMOUNT,
        transaction_type = TRANSACTION_TYPE,
        paid = PAID,
        ignore = IGNORE,
        visible = VISIBLE,
        category_id = CATEGAORY_ID,
        tag_id = TAG_ID,
        account_id_origin = ACCOUNT_ID_ORIGIN,
        account_id_destination = ACCOUNT_ID_DESTINATION,
        created_at = CREATED_AT,
        user_id = USER_ID,
    )


def test_transaction_db_adapter_method_insert(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    transaction_db_adapter.insert(transaction=transaction_model)
    assert REGISTER[0].id == transaction_model.id.hex
    assert REGISTER[0].date == transaction_model.date
    assert REGISTER[0].description == transaction_model.description
    assert REGISTER[0].amount == transaction_model.amount
    assert REGISTER[0].transaction_type == transaction_model.transaction_type.value
    assert REGISTER[0].paid == transaction_model.paid
    assert REGISTER[0].ignore == transaction_model.ignore
    assert REGISTER[0].visible == transaction_model.visible
    assert REGISTER[0].category_id == transaction_model.category_id.hex
    assert REGISTER[0].tag_id == transaction_model.tag_id.hex
    assert REGISTER[0].account_id_origin == transaction_model.account_id_origin.hex
    assert REGISTER[0].account_id_destination == transaction_model.account_id_destination.hex
    assert REGISTER[0].created_at == transaction_model.created_at
    assert REGISTER[0].user_id == transaction_model.user_id.hex


def test_transaction_db_adapter_method_update01(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    new_date = datetime.datetime(year=2002, month=3, day=1, hour=18, minute=15, second=0, microsecond=100)
    new_description = "TESTER_NEW_DESCRIPTION"
    new_amount = Decimal("2.00")
    new_type = TransactionTypes.EXPENSE
    new_paid = False
    new_ignore = False
    new_visible = False
    
    
    transaction_model.date = new_date
    transaction_model.description = new_description
    transaction_model.amount = new_amount
    transaction_model.transaction_type = new_type
    transaction_model.paid = new_paid
    transaction_model.ignore = new_ignore
    transaction_model.visible = new_visible
    
    transaction_db_adapter.update(id=transaction_model.id, transaction=transaction_model)
    assert REGISTER[0].id == transaction_model.id.hex
    assert REGISTER[0].date == new_date
    assert REGISTER[0].description == new_description
    assert REGISTER[0].amount == new_amount
    assert REGISTER[0].transaction_type == new_type.value
    assert REGISTER[0].paid == new_paid
    assert REGISTER[0].ignore == new_ignore
    assert REGISTER[0].visible == new_visible
    assert REGISTER[0].category_id == transaction_model.category_id.hex
    assert REGISTER[0].tag_id == transaction_model.tag_id.hex
    assert REGISTER[0].account_id_origin == transaction_model.account_id_origin.hex
    assert REGISTER[0].account_id_destination == transaction_model.account_id_destination.hex
    assert REGISTER[0].created_at == transaction_model.created_at
    assert REGISTER[0].user_id == transaction_model.user_id.hex


def test_transaction_db_adapter_method_update02(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    new_category_id = uuid.uuid4()
    new_tag_id = uuid.uuid4()
    new_account_id_origin = uuid.uuid4()
    new_account_id_destination = uuid.uuid4()
    new_created_at = datetime.datetime(year=2002, month=3, day=1, hour=18, minute=15, second=0, microsecond=100)
    new_user_id = uuid.uuid4()
    
    transaction_model.category_id = new_category_id
    transaction_model.tag_id = new_tag_id
    transaction_model.account_id_origin = new_account_id_origin
    transaction_model.account_id_destination = new_account_id_destination
    transaction_model.created_at = new_created_at
    transaction_model.user_id = new_user_id
    
    transaction_db_adapter.update(id=transaction_model.id, transaction=transaction_model)
    
    assert REGISTER[0].id == transaction_model.id.hex
    assert REGISTER[0].date == transaction_model.date
    assert REGISTER[0].description == transaction_model.description
    assert REGISTER[0].amount == transaction_model.amount
    assert REGISTER[0].transaction_type == transaction_model.transaction_type.value
    assert REGISTER[0].paid == transaction_model.paid
    assert REGISTER[0].ignore == transaction_model.ignore
    assert REGISTER[0].visible == transaction_model.visible
    assert REGISTER[0].category_id == transaction_model.category_id.hex
    assert REGISTER[0].tag_id == transaction_model.tag_id.hex
    assert REGISTER[0].account_id_origin == transaction_model.account_id_origin.hex
    assert REGISTER[0].account_id_destination == transaction_model.account_id_destination.hex
    assert REGISTER[0].created_at == transaction_model.created_at
    assert REGISTER[0].user_id == transaction_model.user_id.hex


def test_transaction_db_adapter_method_get_all(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    result = transaction_db_adapter.get_all()
    
    assert len(result) == 1
    assert result[0].id.hex == REGISTER[0].id
    assert result[0].date == REGISTER[0].date
    assert result[0].description == REGISTER[0].description
    assert result[0].amount == REGISTER[0].amount
    assert result[0].transaction_type.value == REGISTER[0].transaction_type
    assert result[0].paid == REGISTER[0].paid
    assert result[0].ignore == REGISTER[0].ignore
    assert result[0].visible == REGISTER[0].visible
    assert result[0].category_id.hex == REGISTER[0].category_id
    assert result[0].tag_id.hex == REGISTER[0].tag_id
    assert result[0].account_id_origin.hex == REGISTER[0].account_id_origin
    assert result[0].account_id_destination.hex == REGISTER[0].account_id_destination
    assert result[0].created_at == REGISTER[0].created_at
    assert result[0].user_id.hex == REGISTER[0].user_id


def test_transaction_db_adapter_method_get(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    result = transaction_db_adapter.get(id=transaction_model.id)
    assert result.id.hex == REGISTER[0].id
    assert result.date == REGISTER[0].date
    assert result.description == REGISTER[0].description
    assert result.amount == REGISTER[0].amount
    assert result.transaction_type.value == REGISTER[0].transaction_type
    assert result.paid == REGISTER[0].paid
    assert result.ignore == REGISTER[0].ignore
    assert result.visible == REGISTER[0].visible
    assert result.category_id.hex == REGISTER[0].category_id
    assert result.tag_id.hex == REGISTER[0].tag_id
    assert result.account_id_origin.hex == REGISTER[0].account_id_origin
    assert result.account_id_destination.hex == REGISTER[0].account_id_destination
    assert result.created_at == REGISTER[0].created_at
    assert result.user_id.hex == REGISTER[0].user_id


def test_transaction_db_adapter_method_delete(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    assert len(REGISTER) == 1
    transaction_db_adapter.delete(id=transaction_model.id)
    assert len(REGISTER) == 0


def test_transaction_db_adapter_error_account_already_exists_method_insert(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    with pytest.raises(TransactionAlreadyExistsError):
        transaction_db_adapter.insert(transaction=transaction_model)
        transaction_db_adapter.insert(transaction=transaction_model)


def test_transaction_db_adapter_error_account_not_found_method_update(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    with pytest.raises(TransactionNotFoundError):
        transaction_db_adapter.update(id=uuid.uuid4(), transaction=transaction_model)


def test_transaction_db_adapter_error_generic_method_update_01(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    mock = MockUserRepository()
    mock.select_from_id = lambda id: Transaction(
        id=uuid.uuid4().hex,
        date = datetime.datetime.now(),
        description = "TESTE_DESCRIPTION",
        amount = 2.0,
        transaction_type = "despesa",
        paid = False,
        ignore = True,
        visible = False,
        category_id = uuid.uuid4().hex,
        tag_id = uuid.uuid4().hex,
        account_id_origin = uuid.uuid4().hex,
        account_id_destination = uuid.uuid4().hex,
        created_at = datetime.datetime.now(),
        user_id = uuid.uuid4().hex,
    )
    transaction_db_adapter._db = mock
    with pytest.raises(TransactionDBAdapterError, match="Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'transaction'"):
        transaction_db_adapter.update(id=uuid.uuid4(), transaction=transaction_model)


def test_transaction_db_adapter_error_generic_method_update_02(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    mock = MockUserRepository()
    mock.update = lambda id, date, description, amount, transaction_type, paid, ignore, visible, category_id, tag_id, account_id_origin, account_id_destination, created_at, user_id: None
    transaction_db_adapter._db = mock
    transaction_model.description = "TESTER_RETURN_ERROR"
    with pytest.raises(TransactionDBAdapterError, match="Falha ao tentar atualizar 'Transaction'"):
        transaction_db_adapter.update(id=transaction_model.id, transaction=transaction_model)


def test_transaction_db_adapter_error_unexpected_argument_type_method_insert(transaction_db_adapter: TransactionDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_db_adapter.insert(transaction="TESTER_ERROR")


def test_transaction_db_adapter_error_unexpected_argument_type_method_update(transaction_db_adapter: TransactionDatabaseAdapter, transaction_model: TransactionModel):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_db_adapter.update(id="TESTER_ERROR", transaction=transaction_model)
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_db_adapter.update(id=transaction_model.id, transaction="TESTER_ERROR")


def test_transaction_db_adapter_error_unexpected_argument_type_method_get(transaction_db_adapter: TransactionDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_db_adapter.get(id="TESTER_ERROR")


def test_transaction_db_adapter_error_unexpected_argument_type_method_delete(transaction_db_adapter: TransactionDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_db_adapter.delete(id="TESTER_ERROR")
