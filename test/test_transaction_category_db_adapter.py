import pytest
import uuid
import datetime

from decimal import Decimal
from typing import Optional, List

from infra.entities import TransactionCategory
from src.financial.database_adapter import TransactionCategoryDatabaseAdapter
from src.financial.models import TransactionCategoryModel
from src.financial.exceptions.database_adapter_errors.transaction_category_db_adapter_error import TransactionCategoryAlreadyExistsError, TransactionCategoryDBAdapterError, TransactionCategoryNotFoundError, UnexpectedArgumentTypeError


REGISTER = []

TRANSACTION_CATEGORY_ID = uuid.uuid4()
NAME = "TESTER NAME"
CREATED_AT = datetime.datetime.now()
USER_ID = uuid.uuid4()


class MockUserRepository:
    def __init__(self) -> None:
        self.register = REGISTER
    
    def select(self) -> List[TransactionCategory]:
        return self.register
    
    def select_from_id(self, id: str) -> Optional[TransactionCategory]:
        return next((transaction_category for transaction_category in self.register if transaction_category.id == id), None)
    
    def insert(self,
            id: str,
            name: str,
            created_at: datetime,
            user_id: str) -> TransactionCategory:
        new_transaction_category = TransactionCategory(
            id=id,
            name=name,
            created_at=created_at,
            user_id=user_id,
        )
        self.register.append(new_transaction_category)
        return new_transaction_category
    
    def update(self,
            id: str = None,
            name: str = None,
            created_at: datetime.datetime = None,
            user_id: str = None) -> Optional[TransactionCategory]:
        transaction_category = next((transaction_category for transaction_category in self.register if transaction_category.id == id), None)
        idx = self.register.index(transaction_category)
        
        if not transaction_category:
            return None
        
        fields_to_update = {
                "name": name,
                "created_at": created_at,
                "user_id": user_id,
            }
            
        for field, value in fields_to_update.items():
            if value is not None:
                setattr(transaction_category, field, value)
        self.register.pop(idx)
        self.register.insert(idx, transaction_category)
        return self.select_from_id(id=id)
    
    def delete(self, id: str) -> None:
        self.register.remove(next((transaction_category for transaction_category in self.register if transaction_category.id == id), None))


@pytest.fixture
def transaction_category_db_adapter():
    mocked = TransactionCategoryDatabaseAdapter
    mocked._db = MockUserRepository()
    return mocked


@pytest.fixture
def transaction_category_model():
    return TransactionCategoryModel(
        id=TRANSACTION_CATEGORY_ID,
        name=NAME,
        created_at=CREATED_AT,
        user_id=USER_ID
    )


def test_transaction_category_db_adapter_method_insert(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    transaction_category_db_adapter.insert(transaction_category=transaction_category_model)
    assert REGISTER[0].id == transaction_category_model.id.hex
    assert REGISTER[0].name == transaction_category_model.name
    assert REGISTER[0].created_at == transaction_category_model.created_at
    assert REGISTER[0].user_id == transaction_category_model.user_id.hex


def test_transaction_category_db_adapter_method_update01(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    new_name = "TESTER_UPDATE_NAME"
    transaction_category_model.name = new_name
    transaction_category_db_adapter.update(id=transaction_category_model.id, transaction_category=transaction_category_model)
    assert REGISTER[0].id == transaction_category_model.id.hex
    assert REGISTER[0].name == new_name
    assert REGISTER[0].created_at == transaction_category_model.created_at
    assert REGISTER[0].user_id == transaction_category_model.user_id.hex


def test_transaction_category_db_adapter_method_update02(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    new_created_at = datetime.datetime(year=2002, month=3, day=1, hour=18, minute=15, second=0, microsecond=0)
    new_user_id = uuid.uuid4()
    transaction_category_model.created_at = new_created_at
    transaction_category_model.user_id = new_user_id
    transaction_category_db_adapter.update(id=transaction_category_model.id, transaction_category=transaction_category_model)
    assert REGISTER[0].id == transaction_category_model.id.hex
    assert REGISTER[0].name == transaction_category_model.name
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].user_id == new_user_id.hex


def test_transaction_category_db_adapter_method_get_all(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    result = transaction_category_db_adapter.get_all()
    assert len(result) == 1
    assert result[0].id.hex == REGISTER[0].id
    assert result[0].name == REGISTER[0].name
    assert result[0].created_at == REGISTER[0].created_at
    assert result[0].user_id.hex == REGISTER[0].user_id


def test_transaction_category_db_adapter_method_get(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    result = transaction_category_db_adapter.get(id=transaction_category_model.id)
    assert result.id.hex == REGISTER[0].id
    assert result.name == REGISTER[0].name
    assert result.created_at == REGISTER[0].created_at
    assert result.user_id.hex == REGISTER[0].user_id


def test_transaction_category_db_adapter_method_delete(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    assert len(REGISTER) == 1
    transaction_category_db_adapter.delete(id=transaction_category_model.id)
    assert len(REGISTER) == 0


def test_transaction_category_db_adapter_error_transaction_category_already_exists_method_insert(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    with pytest.raises(TransactionCategoryAlreadyExistsError):
        transaction_category_db_adapter.insert(transaction_category=transaction_category_model)
        transaction_category_db_adapter.insert(transaction_category=transaction_category_model)


def test_transaction_category_db_adapter_error_transaction_category_not_found_method_update(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    with pytest.raises(TransactionCategoryNotFoundError):
        transaction_category_db_adapter.update(id=uuid.uuid4(), transaction_category=transaction_category_model)


def test_transaction_category_db_adapter_error_generic_method_update_01(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    mock = MockUserRepository()
    mock.select_from_id = lambda id: TransactionCategory(
        id=uuid.uuid4().hex,
        name="TESTER NAME",
        created_at=datetime.datetime.now(),
        user_id=uuid.uuid4().hex,
    )
    transaction_category_db_adapter._db = mock
    with pytest.raises(TransactionCategoryDBAdapterError, match="Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'transaction_category'"):
        transaction_category_db_adapter.update(id=uuid.uuid4(), transaction_category=transaction_category_model)


def test_transaction_category_db_adapter_error_generic_method_update_02(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    mock = MockUserRepository()
    mock.update = lambda id, name, created_at, user_id: None
    transaction_category_db_adapter._db = mock
    transaction_category_model.name = "TESTER_RETURN_ERROR"
    with pytest.raises(TransactionCategoryDBAdapterError, match="Falha ao tentar atualizar 'TransactionCategory'"):
        transaction_category_db_adapter.update(id=transaction_category_model.id, transaction_category=transaction_category_model)


def test_transaction_category_db_adapter_error_unexpected_argument_type_method_insert(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_category_db_adapter.insert(transaction_category="TESTER_ERROR")


def test_transaction_category_db_adapter_error_unexpected_argument_type_method_update(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter, transaction_category_model: TransactionCategoryModel):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_category_db_adapter.update(id="TESTER_ERROR", transaction_category=transaction_category_model)
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_category_db_adapter.update(id=transaction_category_model.id, transaction_category="TESTER_ERROR")


def test_transaction_category_db_adapter_error_unexpected_argument_type_method_get(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_category_db_adapter.get(id="TESTER_ERROR")


def test_transaction_category_db_adapter_error_unexpected_argument_type_method_delete(transaction_category_db_adapter: TransactionCategoryDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_category_db_adapter.delete(id="TESTER_ERROR")
