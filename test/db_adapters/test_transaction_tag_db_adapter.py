import pytest
import uuid
import datetime

from typing import Optional, List

from infra.entities import TransactionTag
from src.financial.database_adapter import TransactionTagDatabaseAdapter
from src.financial.models import TransactionTagModel
from src.financial.exceptions.database_adapter_errors.transaction_tag_db_adapter_error import TransactionTagAlreadyExistsError, TransactionTagDBAdapterError, TransactionTagNotFoundError, UnexpectedArgumentTypeError


REGISTER = []

TRANSACTION_TAG_ID = uuid.uuid4()
NAME = "TESTER NAME"
CREATED_AT = datetime.datetime.now()
USER_ID = uuid.uuid4()


class MockUserRepository:
    def __init__(self) -> None:
        self.register = REGISTER
    
    def select(self) -> List[TransactionTag]:
        return self.register
    
    def select_from_id(self, id: str) -> Optional[TransactionTag]:
        return next((transaction_tag for transaction_tag in self.register if transaction_tag.id == id), None)
    
    def insert(self,
            id: str,
            name: str,
            created_at: datetime,
            user_id: str) -> TransactionTag:
        new_transaction_tag = TransactionTag(
            id=id,
            name=name,
            created_at=created_at,
            user_id=user_id,
        )
        self.register.append(new_transaction_tag)
        return new_transaction_tag
    
    def update(self,
            id: str = None,
            name: str = None,
            created_at: datetime.datetime = None,
            user_id: str = None) -> Optional[TransactionTag]:
        transaction_tag = next((transaction_tag for transaction_tag in self.register if transaction_tag.id == id), None)
        idx = self.register.index(transaction_tag)
        
        if not transaction_tag:
            return None
        
        fields_to_update = {
                "name": name,
                "created_at": created_at,
                "user_id": user_id,
            }
            
        for field, value in fields_to_update.items():
            if value is not None:
                setattr(transaction_tag, field, value)
        self.register.pop(idx)
        self.register.insert(idx, transaction_tag)
        return self.select_from_id(id=id)
    
    def delete(self, id: str) -> None:
        self.register.remove(next((transaction_tag for transaction_tag in self.register if transaction_tag.id == id), None))


@pytest.fixture
def transaction_tag_db_adapter():
    mocked = TransactionTagDatabaseAdapter
    mocked._db = MockUserRepository()
    return mocked


@pytest.fixture
def transaction_tag_model():
    return TransactionTagModel(
        id=TRANSACTION_TAG_ID,
        name=NAME,
        created_at=CREATED_AT,
        user_id=USER_ID
    )


def test_transaction_tag_db_adapter_method_insert(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    transaction_tag_db_adapter.insert(transaction_tag=transaction_tag_model)
    assert REGISTER[0].id == transaction_tag_model.id.hex
    assert REGISTER[0].name == transaction_tag_model.name
    assert REGISTER[0].created_at == transaction_tag_model.created_at
    assert REGISTER[0].user_id == transaction_tag_model.user_id.hex


def test_transaction_tag_db_adapter_method_update01(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    new_name = "TESTER_UPDATE_NAME"
    transaction_tag_model.name = new_name
    transaction_tag_db_adapter.update(id=transaction_tag_model.id, transaction_tag=transaction_tag_model)
    assert REGISTER[0].id == transaction_tag_model.id.hex
    assert REGISTER[0].name == new_name
    assert REGISTER[0].created_at == transaction_tag_model.created_at
    assert REGISTER[0].user_id == transaction_tag_model.user_id.hex


def test_transaction_tag_db_adapter_method_update02(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    new_created_at = datetime.datetime(year=2002, month=3, day=1, hour=18, minute=15, second=0, microsecond=0)
    new_user_id = uuid.uuid4()
    transaction_tag_model.created_at = new_created_at
    transaction_tag_model.user_id = new_user_id
    transaction_tag_db_adapter.update(id=transaction_tag_model.id, transaction_tag=transaction_tag_model)
    assert REGISTER[0].id == transaction_tag_model.id.hex
    assert REGISTER[0].name == transaction_tag_model.name
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].user_id == new_user_id.hex


def test_transaction_tag_db_adapter_method_get_all(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    result = transaction_tag_db_adapter.get_all()
    assert len(result) == 1
    assert result[0].id.hex == REGISTER[0].id
    assert result[0].name == REGISTER[0].name
    assert result[0].created_at == REGISTER[0].created_at
    assert result[0].user_id.hex == REGISTER[0].user_id


def test_transaction_tag_db_adapter_method_get(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    result = transaction_tag_db_adapter.get(id=transaction_tag_model.id)
    assert result.id.hex == REGISTER[0].id
    assert result.name == REGISTER[0].name
    assert result.created_at == REGISTER[0].created_at
    assert result.user_id.hex == REGISTER[0].user_id


def test_transaction_tag_db_adapter_method_delete(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    assert len(REGISTER) == 1
    transaction_tag_db_adapter.delete(id=transaction_tag_model.id)
    assert len(REGISTER) == 0


def test_transaction_tag_db_adapter_error_transaction_tag_already_exists_method_insert(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    with pytest.raises(TransactionTagAlreadyExistsError):
        transaction_tag_db_adapter.insert(transaction_tag=transaction_tag_model)
        transaction_tag_db_adapter.insert(transaction_tag=transaction_tag_model)


def test_transaction_tag_db_adapter_error_transaction_tag_not_found_method_update(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    with pytest.raises(TransactionTagNotFoundError):
        transaction_tag_db_adapter.update(id=uuid.uuid4(), transaction_tag=transaction_tag_model)


def test_transaction_tag_db_adapter_error_generic_method_update_01(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    mock = MockUserRepository()
    mock.select_from_id = lambda id: TransactionTag(
        id=uuid.uuid4().hex,
        name="TESTER NAME",
        created_at=datetime.datetime.now(),
        user_id=uuid.uuid4().hex,
    )
    transaction_tag_db_adapter._db = mock
    with pytest.raises(TransactionTagDBAdapterError, match="Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'transaction_tag'"):
        transaction_tag_db_adapter.update(id=uuid.uuid4(), transaction_tag=transaction_tag_model)


def test_transaction_tag_db_adapter_error_generic_method_update_02(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    mock = MockUserRepository()
    mock.update = lambda id, name, created_at, user_id: None
    transaction_tag_db_adapter._db = mock
    transaction_tag_model.name = "TESTER_RETURN_ERROR"
    with pytest.raises(TransactionTagDBAdapterError, match="Falha ao tentar atualizar 'TransactionTag'"):
        transaction_tag_db_adapter.update(id=transaction_tag_model.id, transaction_tag=transaction_tag_model)


def test_transaction_tag_db_adapter_error_unexpected_argument_type_method_insert(transaction_tag_db_adapter: TransactionTagDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_tag_db_adapter.insert(transaction_tag="TESTER_ERROR")


def test_transaction_tag_db_adapter_error_unexpected_argument_type_method_update(transaction_tag_db_adapter: TransactionTagDatabaseAdapter, transaction_tag_model: TransactionTagModel):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_tag_db_adapter.update(id="TESTER_ERROR", transaction_tag=transaction_tag_model)
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_tag_db_adapter.update(id=transaction_tag_model.id, transaction_tag="TESTER_ERROR")


def test_transaction_tag_db_adapter_error_unexpected_argument_type_method_get(transaction_tag_db_adapter: TransactionTagDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_tag_db_adapter.get(id="TESTER_ERROR")


def test_transaction_tag_db_adapter_error_unexpected_argument_type_method_delete(transaction_tag_db_adapter: TransactionTagDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        transaction_tag_db_adapter.delete(id="TESTER_ERROR")
