import pytest
import uuid

from datetime import datetime
from typing import Optional, List

from src.financial.models import UserModel
from src.financial.handlers import UserHandler
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.handler_errors import user_handler_error


REGISTER = []


class MockUserDatabaseAdapter(DatabaseAdapterInterface):
    _db = None
    @classmethod
    def insert(cls, user) -> None:
        REGISTER.append(user)
        return True
    
    @classmethod
    def update(cls, id, user) -> None:
        result = next((user for user in REGISTER if user.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
        REGISTER.insert(idx, user)
    
    @classmethod
    def delete(cls, id) -> None:
        result = next((user for user in REGISTER if user.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
    
    @classmethod
    def get(cls, id) -> Optional[UserModel]:
        return next((user for user in REGISTER if user.id == id), None)
    
    @classmethod
    def get_all(cls) -> List[UserModel]:
        return REGISTER


@pytest.fixture
def user_model():
    return UserModel(nickname="TESTER")


@pytest.fixture
def user_handler():
    return UserHandler(database=MockUserDatabaseAdapter)


# Testa a instancia se ta ok
def test_user_handler_istance(user_handler: UserHandler):
    assert isinstance(user_handler, UserHandler) == True
    assert issubclass(user_handler._database, DatabaseAdapterInterface)


# Testa se está criando a usuário normalmente
def test_user_handler_create_user(user_handler: UserHandler, user_model: UserModel):
    user_handler.create_user(user=user_model)
    assert isinstance(REGISTER[0], UserModel) == True


# Testa se ta atualizando normal
def test_user_handler_update_user(user_handler: UserHandler, user_model: UserModel):
    new_nickname = "TESTER UPDATE"
    new_created_at = user_model.created_at
    
    user_model.nickname = new_nickname
    user_model.created_at = new_created_at
    
    user_handler.update_user(id= REGISTER[0].id, user=user_model)
    
    assert isinstance(REGISTER[0], UserModel) == True
    assert REGISTER[0].nickname == new_nickname
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].id == user_model.id


# Testa se ta retornando a usuário normalmente
def test_user_handler_get_user(user_handler: UserHandler):
    user = user_handler.get_user(id=REGISTER[0].id)
    assert isinstance(user, UserModel) == True
    assert user.id == REGISTER[0].id


# Testa se esta recebendo todas as usuários registrada
def test_user_handler_get_all_users(user_handler: UserHandler):
    accounts = user_handler.get_all_users()
    assert len(accounts) == 1


# Testa se os changers estão funcionando
def test_user_handler_changers_account_properts(user_handler: UserHandler, user_model: UserModel):
    id = REGISTER[0].id
    new_nickname = "USER CHANGER"
    new_created_at = user_model.created_at
    
    user_handler.change_created_at(id=id, created_at=new_created_at)
    user_handler.change_nickname(id=id, nickname=new_nickname)
    
    assert REGISTER[0].id == id
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].nickname == new_nickname


# Testa se o delete ta funcionando
def test_user_handler_delete_user(user_handler: UserHandler):
    user_handler.delete_user(id=REGISTER[0].id)
    assert len(REGISTER) == 0


# Testa o erro de tipo do database em propriedade
def test_user_handler_database_type_error_01(user_handler: UserHandler):
    with pytest.raises(user_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'value'"):
        user_handler.database = "TESTE STRING TYPE"


# Testa o erro de tipo do database ao istanciar
def test_user_handler_database_type_error_02():
    with pytest.raises(user_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'databese'"):
        UserHandler(database="TESTE STRING TYPE")


# Testa o erro de tipo ao criar usuário
def test_user_handler_unexpected_type_error_create_user(user_handler: UserHandler):
    with pytest.raises(user_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'user'"):
        user_handler.create_user(user="TESTE STRING TYPE")


# Testa o erro de tipo ao atualizar usuário
def test_user_handler_unexpected_type_error_update_user(user_handler: UserHandler, user_model: UserModel):
    with pytest.raises(user_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        user_handler.update_user(id="TESTE STRING TYPE", user=user_model)
    with pytest.raises(user_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'user'"):
        user_handler.update_user(id=uuid.uuid4(), user="TESTE STRING TYPE")


# Testa o erro de tipo ao deletar usuário
def test_user_handler_unexpected_type_error_delete_user(user_handler: UserHandler):
    with pytest.raises(user_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        user_handler.delete_user(id="TESTE STRING TYPE")


# Testa o erro de tipo ao receber usuário
def test_user_handler_unexpected_type_error_get_user(user_handler: UserHandler):
    with pytest.raises(user_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        user_handler.get_user(id="TESTE STRING TYPE")


# Testa o erro de tipo ao mudar descrição da usuário
def test_user_handler_unexpected_type_error_change_nickname(user_handler: UserHandler):
    with pytest.raises(user_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        user_handler.change_nickname(id="TESTE STRING TYPE", nickname="BLA BLA")
    with pytest.raises(user_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'nickname'"):
        user_handler.change_nickname(id=uuid.uuid4(), nickname=1.0)


# Testa o erro de tipo ao mudar data de criação da usuário
def test_user_handler_unexpected_type_error_change_created_at(user_handler: UserHandler):
    with pytest.raises(user_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        user_handler.change_created_at(id="TESTE STRING TYPE", created_at=datetime.now())
    with pytest.raises(user_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'created_at'"):
        user_handler.change_created_at(id=uuid.uuid4(), created_at="TESTE STRING TYPE")
