import pytest
import uuid
import datetime

from typing import Optional, List

from infra.entities import AccountTag
from src.financial.database_adapter import AccountTagDatabaseAdapter
from src.financial.models import AccountTagModel
from src.financial.exceptions.database_adapter_errors.account_tag_db_adapter_error import AccountTagAlreadyExistsError, AccountTagDBAdapterError, AccountTagNotFoundError, UnexpectedArgumentTypeError


REGISTER = []

ACCOUNT_TAG_ID = uuid.uuid4()
NAME = "TESTER NAME"
CREATED_AT = datetime.datetime.now()
USER_ID = uuid.uuid4()


class MockUserRepository:
    def __init__(self) -> None:
        self.register = REGISTER
    
    def select(self) -> List[AccountTag]:
        return self.register
    
    def select_from_id(self, id: str) -> Optional[AccountTag]:
        return next((account_tag for account_tag in self.register if account_tag.id == id), None)
    
    def insert(self,
            id: str,
            name: str,
            created_at: datetime,
            user_id: str) -> AccountTag:
        new_account_tag = AccountTag(
            id=id,
            name=name,
            created_at=created_at,
            user_id=user_id,
        )
        self.register.append(new_account_tag)
        return new_account_tag
    
    def update(self,
            id: str = None,
            name: str = None,
            created_at: datetime.datetime = None,
            user_id: str = None) -> Optional[AccountTag]:
        account_tag = next((account_tag for account_tag in self.register if account_tag.id == id), None)
        idx = self.register.index(account_tag)
        
        if not account_tag:
            return None
        
        fields_to_update = {
                "name": name,
                "created_at": created_at,
                "user_id": user_id,
            }
            
        for field, value in fields_to_update.items():
            if value is not None:
                setattr(account_tag, field, value)
        self.register.pop(idx)
        self.register.insert(idx, account_tag)
        return self.select_from_id(id=id)
    
    def delete(self, id: str) -> None:
        self.register.remove(next((account_tag for account_tag in self.register if account_tag.id == id), None))


@pytest.fixture
def account_tag_db_adapter():
    mocked = AccountTagDatabaseAdapter
    mocked._db = MockUserRepository()
    return mocked


@pytest.fixture
def account_tag_model():
    return AccountTagModel(
        id=ACCOUNT_TAG_ID,
        name=NAME,
        created_at=CREATED_AT,
        user_id=USER_ID
    )


def test_account_tag_db_adapter_method_insert(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    account_tag_db_adapter.insert(account_tag=account_tag_model)
    assert REGISTER[0].id == account_tag_model.id.hex
    assert REGISTER[0].name == account_tag_model.name
    assert REGISTER[0].created_at == account_tag_model.created_at
    assert REGISTER[0].user_id == account_tag_model.user_id.hex


def test_account_tag_db_adapter_method_update01(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    new_name = "TESTER_UPDATE_NAME"
    account_tag_model.name = new_name
    account_tag_db_adapter.update(id=account_tag_model.id, account_tag=account_tag_model)
    assert REGISTER[0].id == account_tag_model.id.hex
    assert REGISTER[0].name == new_name
    assert REGISTER[0].created_at == account_tag_model.created_at
    assert REGISTER[0].user_id == account_tag_model.user_id.hex


def test_account_tag_db_adapter_method_update02(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    new_created_at = datetime.datetime(year=2002, month=3, day=1, hour=18, minute=15, second=0, microsecond=0)
    new_user_id = uuid.uuid4()
    account_tag_model.created_at = new_created_at
    account_tag_model.user_id = new_user_id
    account_tag_db_adapter.update(id=account_tag_model.id, account_tag=account_tag_model)
    assert REGISTER[0].id == account_tag_model.id.hex
    assert REGISTER[0].name == account_tag_model.name
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].user_id == new_user_id.hex


def test_account_tag_db_adapter_method_get_all(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    result = account_tag_db_adapter.get_all()
    assert len(result) == 1
    assert result[0].id.hex == REGISTER[0].id
    assert result[0].name == REGISTER[0].name
    assert result[0].created_at == REGISTER[0].created_at
    assert result[0].user_id.hex == REGISTER[0].user_id


def test_account_tag_db_adapter_method_get(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    result = account_tag_db_adapter.get(id=account_tag_model.id)
    assert result.id.hex == REGISTER[0].id
    assert result.name == REGISTER[0].name
    assert result.created_at == REGISTER[0].created_at
    assert result.user_id.hex == REGISTER[0].user_id


def test_account_tag_db_adapter_method_delete(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    assert len(REGISTER) == 1
    account_tag_db_adapter.delete(id=account_tag_model.id)
    assert len(REGISTER) == 0


def test_account_tag_db_adapter_error_account_tag_already_exists_method_insert(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    with pytest.raises(AccountTagAlreadyExistsError):
        account_tag_db_adapter.insert(account_tag=account_tag_model)
        account_tag_db_adapter.insert(account_tag=account_tag_model)


def test_account_tag_db_adapter_error_account_tag_not_found_method_update(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    with pytest.raises(AccountTagNotFoundError):
        account_tag_db_adapter.update(id=uuid.uuid4(), account_tag=account_tag_model)


def test_account_tag_db_adapter_error_generic_method_update_01(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    mock = MockUserRepository()
    mock.select_from_id = lambda id: AccountTag(
        id=uuid.uuid4().hex,
        name="TESTER NAME",
        created_at=datetime.datetime.now(),
        user_id=uuid.uuid4().hex,
    )
    account_tag_db_adapter._db = mock
    with pytest.raises(AccountTagDBAdapterError, match="Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'account_tag'"):
        account_tag_db_adapter.update(id=uuid.uuid4(), account_tag=account_tag_model)


def test_account_tag_db_adapter_error_generic_method_update_02(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    mock = MockUserRepository()
    mock.update = lambda id, name, created_at, user_id: None
    account_tag_db_adapter._db = mock
    account_tag_model.name = "TESTER_RETURN_ERROR"
    with pytest.raises(AccountTagDBAdapterError, match="Falha ao tentar atualizar 'AccountTag'"):
        account_tag_db_adapter.update(id=account_tag_model.id, account_tag=account_tag_model)


def test_account_tag_db_adapter_error_unexpected_argument_type_method_insert(account_tag_db_adapter: AccountTagDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        account_tag_db_adapter.insert(account_tag="TESTER_ERROR")


def test_account_tag_db_adapter_error_unexpected_argument_type_method_update(account_tag_db_adapter: AccountTagDatabaseAdapter, account_tag_model: AccountTagModel):
    with pytest.raises(UnexpectedArgumentTypeError):
        account_tag_db_adapter.update(id="TESTER_ERROR", account_tag=account_tag_model)
    with pytest.raises(UnexpectedArgumentTypeError):
        account_tag_db_adapter.update(id=account_tag_model.id, account_tag="TESTER_ERROR")


def test_account_tag_db_adapter_error_unexpected_argument_type_method_get(account_tag_db_adapter: AccountTagDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        account_tag_db_adapter.get(id="TESTER_ERROR")


def test_account_tag_db_adapter_error_unexpected_argument_type_method_delete(account_tag_db_adapter: AccountTagDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        account_tag_db_adapter.delete(id="TESTER_ERROR")
