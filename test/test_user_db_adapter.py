import pytest
import uuid
import datetime

from typing import Optional, List

from infra.entities import User
from src.financial.database_adapter.user_db_adapter import UserDatabaseAdapter
from src.financial.models.user_model import UserModel
from src.financial.exceptions.database_adapter_errors.user_db_adapter_error import UserAlreadyExistsError, UserDBAdapterError, UnexpectedArgumentTypeError, UserNotFoundError


REGISTER = []
USER_ID = uuid.uuid4()
NICKNAME = "TESTER"
CREATED_AT = datetime.datetime.now()


class MockUserRepository:
    def __init__(self) -> None:
        self.register = REGISTER
    
    def select(self) -> List[User]:
        return self.register
    
    def select_from_id(self, id: str) -> Optional[User]:
        return next((user for user in self.register if user.id == id), None)
    
    def insert(self, id:str, nickname: str, created_at: datetime) -> User:
        new_user = User(
            id = id,
            nickname = nickname,
            created_at = created_at
        )
        self.register.append(new_user)
        return new_user
    
    def update(self, id:str, nickname:str=None, created_at:datetime=None) -> Optional[User]:
        user = next((user for user in self.register if user.id == id), None)
        idx = self.register.index(user)
        if user:
            if nickname:
                user.nickname = nickname
            if created_at:
                user.created_at = created_at
            self.register.pop(idx)
            self.register.insert(idx, user)
            return self.select_from_id(id=id)
        return None
    
    def delete(self, id: str) -> None:
        self.register.remove(next((user for user in self.register if user.id == id), None))


@pytest.fixture
def user_db_adapter():
    mocked = UserDatabaseAdapter
    mocked._db = MockUserRepository()
    return mocked


@pytest.fixture
def user_model():
    return UserModel(id=USER_ID, nickname=NICKNAME, created_at=CREATED_AT)


def test_user_db_adapter_method_insert(user_db_adapter: UserDatabaseAdapter, user_model: UserModel):
    user_db_adapter.insert(user=user_model)
    assert REGISTER[0].id == user_model.id.hex
    assert REGISTER[0].nickname == user_model.nickname
    assert REGISTER[0].created_at == user_model.created_at


def test_user_db_adapter_method_update(user_db_adapter: UserDatabaseAdapter, user_model: UserModel):
    new_nickname = "TESTER_UPDATE"
    new_created_at = datetime.datetime(year=2002, month=3, day=1, hour=18, minute=15, second=0, microsecond=0)
    user_model.nickname = new_nickname
    user_model.created_at = new_created_at
    user_db_adapter.update(id=user_model.id, user=user_model)
    assert REGISTER[0].id == user_model.id.hex
    assert REGISTER[0].nickname == new_nickname
    assert REGISTER[0].created_at == new_created_at


def test_user_db_adapter_method_get_all(user_db_adapter: UserDatabaseAdapter, user_model: UserModel):
    result = user_db_adapter.get_all()
    assert len(result) == 1
    assert result[0].id.hex == REGISTER[0].id
    assert result[0].nickname == REGISTER[0].nickname
    assert result[0].created_at == REGISTER[0].created_at


def test_user_db_adapter_method_get(user_db_adapter: UserDatabaseAdapter, user_model: UserModel):
    result = user_db_adapter.get(id=user_model.id)
    assert result.id.hex == REGISTER[0].id
    assert result.nickname == REGISTER[0].nickname
    assert result.created_at == REGISTER[0].created_at


def test_user_db_adapter_method_delete(user_db_adapter: UserDatabaseAdapter, user_model: UserModel):
    assert len(REGISTER) == 1
    user_db_adapter.delete(id=user_model.id)
    assert len(REGISTER) == 0


def test_user_db_adapter_error_user_already_exists_method_insert(user_db_adapter: UserDatabaseAdapter, user_model: UserModel):
    with pytest.raises(UserAlreadyExistsError):
        user_db_adapter.insert(user=user_model)
        user_db_adapter.insert(user=user_model)


def test_user_db_adapter_error_user_not_found_method_update(user_db_adapter: UserDatabaseAdapter, user_model: UserModel):
    with pytest.raises(UserNotFoundError):
        user_db_adapter.update(id=uuid.uuid4(), user=user_model)


def test_user_db_adapter_error_generic_method_update_01(user_db_adapter: UserDatabaseAdapter, user_model: UserModel):
    mock = MockUserRepository()
    mock.select_from_id = lambda id: User(id=uuid.uuid4().hex, nickname="TESTER", created_at=datetime.datetime.now())
    user_db_adapter._db = mock
    with pytest.raises(UserDBAdapterError, match="Incosistencia entre o parametro 'id' e a proprienda id do paramentro 'user'"):
        user_db_adapter.update(id=uuid.uuid4(), user=user_model)


def test_user_db_adapter_error_generic_method_update_02(user_db_adapter: UserDatabaseAdapter, user_model: UserModel):
    mock = MockUserRepository()
    mock.update = lambda id, nickname, created_at: None
    user_db_adapter._db = mock
    user_model.nickname = "TESTER_RETURN_ERROR"
    with pytest.raises(UserDBAdapterError, match="Falha ao tentar atualizar 'User'"):
        user_db_adapter.update(id=user_model.id, user=user_model)


def test_user_db_adapter_error_unexpected_argument_type_method_insert(user_db_adapter: UserDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        user_db_adapter.insert(user="TESTER_ERROR")


def test_user_db_adapter_error_unexpected_argument_type_method_update(user_db_adapter: UserDatabaseAdapter, user_model: UserModel):
    with pytest.raises(UnexpectedArgumentTypeError):
        user_db_adapter.update(id="TESTER_ERROR", user=user_model)
    with pytest.raises(UnexpectedArgumentTypeError):
        user_db_adapter.update(id=user_model.id, user="TESTER_ERROR")


def test_user_db_adapter_error_unexpected_argument_type_method_get(user_db_adapter: UserDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        user_db_adapter.get(id="TESTER_ERROR")


def test_user_db_adapter_error_unexpected_argument_type_method_delete(user_db_adapter: UserDatabaseAdapter):
    with pytest.raises(UnexpectedArgumentTypeError):
        user_db_adapter.delete(id="TESTER_ERROR")
