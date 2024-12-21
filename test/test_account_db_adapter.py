import pytest
import uuid
import datetime

from decimal import Decimal
from typing import Optional, List

from infra.entities import Account
from src.financial.database_adapter.account_db_adapter import AccountDatabaseAdapter
from src.financial.models import AccountModel
from src.financial.exceptions.database_adapter_errors.account_db_adapter_error import AccountAlreadyExistsError, AccountDBAdapterError, AccountNotFoundError, UnexpectedArgumentTypeError


REGISTER = []

ACCOUNT_ID = uuid.uuid4()
NAME = "TESTER NAME"
DESCRIPTION = "TESTER ACCOUNT DESCRIPTION"
TAG_ID = uuid.uuid4()
BALANCE = Decimal("0.00")
CREATED_AT = datetime.datetime.now()
USER_ID = uuid.uuid4()


class MockUserRepository:
    def __init__(self) -> None:
        self.register = REGISTER
    
    def select(self) -> List[Account]:
        return self.register
    
    def select_from_id(self, id: str) -> Optional[Account]:
        return next((account for account in self.register if account.id == id), None)
    
    def insert(self,
            id: str,
            name: str,
            description: str,
            tag_id: str,
            balance: float,
            created_at: datetime,
            user_id: str) -> Account:
        new_account = Account(
            id=id,
            name=name,
            description=description,
            tag_id=tag_id,
            balance=balance,
            created_at=created_at,
            user_id=user_id,
        )
        self.register.append(new_account)
        return new_account
    
    def update(self,
            id: str = None,
            name: str = None,
            description: str = None,
            tag_id: str = None,
            balance: float = None,
            created_at: datetime.datetime = None,
            user_id: str = None) -> Optional[Account]:
        account = next((account for account in self.register if account.id == id), None)
        idx = self.register.index(account)
        
        if not account:
            return None
        
        fields_to_update = {
                "name": name,
                "description": description,
                "tag_id": tag_id,
                "balance": balance,
                "created_at": created_at,
                "user_id": user_id,
            }
            
        for field, value in fields_to_update.items():
            if value is not None:
                setattr(account, field, value)
        self.register.pop(idx)
        self.register.insert(idx, account)
        return self.select_from_id(id=id)
    
    def delete(self, id: str) -> None:
        self.register.remove(next((account for account in self.register if account.id == id), None))


@pytest.fixture
def account_db_adapter():
    mocked = AccountDatabaseAdapter
    mocked._db = MockUserRepository()
    return mocked


@pytest.fixture
def account_model():
    return AccountModel(
        id=ACCOUNT_ID,
        name=NAME,
        description=DESCRIPTION,
        tag_id=TAG_ID,
        balance=BALANCE,
        created_at=CREATED_AT,
        user_id=USER_ID
    )


def test_account_db_adapter_method_insert(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    account_db_adapter.insert(account=account_model)
    assert REGISTER[0].id == account_model.id.hex
    assert REGISTER[0].name == account_model.name
    assert REGISTER[0].description == account_model.description
    assert REGISTER[0].tag_id == account_model.tag_id.hex
    assert REGISTER[0].balance == account_model.balance
    assert REGISTER[0].created_at == account_model.created_at
    assert REGISTER[0].user_id == account_model.user_id.hex


def test_account_db_adapter_method_update01(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    new_name = "TESTER_UPDATE_NAME"
    new_description = "TESTER_UPDATE_DESCRIPTION"
    new_tag_id = uuid.uuid4()
    account_model.name = new_name
    account_model.description = new_description
    account_model.tag_id = new_tag_id
    account_db_adapter.update(id=account_model.id, account=account_model)
    assert REGISTER[0].id == account_model.id.hex
    assert REGISTER[0].name == new_name
    assert REGISTER[0].description == new_description
    assert REGISTER[0].tag_id == new_tag_id.hex
    assert REGISTER[0].balance == account_model.balance
    assert REGISTER[0].created_at == account_model.created_at
    assert REGISTER[0].user_id == account_model.user_id.hex


def test_account_db_adapter_method_update02(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    new_balance = Decimal("999.99")
    new_created_at = datetime.datetime(year=2002, month=3, day=1, hour=18, minute=15, second=0, microsecond=0)
    new_user_id = uuid.uuid4()
    account_model.balance = new_balance
    account_model.created_at = new_created_at
    account_model.user_id = new_user_id
    account_db_adapter.update(id=account_model.id, account=account_model)
    assert REGISTER[0].id == account_model.id.hex
    assert REGISTER[0].name == account_model.name
    assert REGISTER[0].description == account_model.description
    assert REGISTER[0].tag_id == account_model.tag_id.hex
    assert REGISTER[0].balance == new_balance
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].user_id == new_user_id.hex


def test_account_db_adapter_method_get_all(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    result = account_db_adapter.get_all()
    assert len(result) == 1
    assert result[0].id.hex == REGISTER[0].id
    assert result[0].name == REGISTER[0].name
    assert result[0].description == REGISTER[0].description
    assert result[0].tag_id.hex == REGISTER[0].tag_id
    assert result[0].balance == REGISTER[0].balance
    assert result[0].created_at == REGISTER[0].created_at
    assert result[0].user_id.hex == REGISTER[0].user_id


def test_account_db_adapter_method_get(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    result = account_db_adapter.get(id=account_model.id)
    assert result.id.hex == REGISTER[0].id
    assert result.name == REGISTER[0].name
    assert result.description == REGISTER[0].description
    assert result.tag_id.hex == REGISTER[0].tag_id
    assert result.balance == REGISTER[0].balance
    assert result.created_at == REGISTER[0].created_at
    assert result.user_id.hex == REGISTER[0].user_id


def test_account_db_adapter_method_delete(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    assert len(REGISTER) == 1
    account_db_adapter.delete(id=account_model.id)
    assert len(REGISTER) == 0


def test_account_db_adapter_error_account_already_exists_method_insert(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    with pytest.raises(AccountAlreadyExistsError):
        account_db_adapter.insert(account=account_model)
        account_db_adapter.insert(account=account_model)


def test_account_db_adapter_error_account_not_found_method_update(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    with pytest.raises(AccountNotFoundError):
        account_db_adapter.update(id=uuid.uuid4(), account=account_model)


def test_account_db_adapter_error_generic_method_update_01(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    mock = MockUserRepository()
    mock.select_from_id = lambda id: Account(
        id=uuid.uuid4().hex,
        name="TESTER NAME",
        description="TESTER DESCRIPTION",
        tag_id=uuid.uuid4().hex,
        balance=2.0,
        created_at=datetime.datetime.now(),
        user_id=uuid.uuid4().hex,
    )
    account_db_adapter._db = mock
    with pytest.raises(AccountDBAdapterError, match="Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'account'"):
        account_db_adapter.update(id=uuid.uuid4(), account=account_model)


def test_account_db_adapter_error_generic_method_update_02(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    mock = MockUserRepository()
    mock.update = lambda id, name, description, tag_id, balance, created_at, user_id: None
    account_db_adapter._db = mock
    account_model.name = "TESTER_RETURN_ERROR"
    with pytest.raises(AccountDBAdapterError, match="Falha ao tentar atualizar 'Account'"):
        account_db_adapter.update(id=account_model.id, account=account_model)


def test_account_db_adapter_error_unexpected_argument_type_method_insert(account_db_adapter: AccountDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        account_db_adapter.insert(account="TESTER_ERROR")


def test_account_db_adapter_error_unexpected_argument_type_method_update(account_db_adapter: AccountDatabaseAdapter, account_model: AccountModel):
    with pytest.raises(UnexpectedArgumentTypeError):
        account_db_adapter.update(id="TESTER_ERROR", account=account_model)
    with pytest.raises(UnexpectedArgumentTypeError):
        account_db_adapter.update(id=account_model.id, account="TESTER_ERROR")


def test_account_db_adapter_error_unexpected_argument_type_method_get(account_db_adapter: AccountDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        account_db_adapter.get(id="TESTER_ERROR")


def test_account_db_adapter_error_unexpected_argument_type_method_delete(account_db_adapter: AccountDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        account_db_adapter.delete(id="TESTER_ERROR")
