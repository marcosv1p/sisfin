import pytest
import uuid

from datetime import datetime
from typing import Optional, List

from src.financial.models import AccountTagModel
from src.financial.handlers import AccountTagHandler
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.handler_errors import account_tag_handler_error


REGISTER = []


class MockAccountTagDatabaseAdapter(DatabaseAdapterInterface):
    _db = None
    @classmethod
    def insert(cls, account_tag) -> None:
        REGISTER.append(account_tag)
        return True
    
    @classmethod
    def update(cls, id, account_tag) -> None:
        result = next((account_tag for account_tag in REGISTER if account_tag.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
        REGISTER.insert(idx, account_tag)
    
    @classmethod
    def delete(cls, id) -> None:
        result = next((account_tag for account_tag in REGISTER if account_tag.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
    
    @classmethod
    def get(cls, id) -> Optional[AccountTagModel]:
        return next((account_tag for account_tag in REGISTER if account_tag.id == id), None)
    
    @classmethod
    def get_all(cls) -> List[AccountTagModel]:
        return REGISTER


@pytest.fixture
def account_tag_model():
    return AccountTagModel(name="Minha Tag Teste", user_id=uuid.uuid4())


@pytest.fixture
def account_tag_handler():
    return AccountTagHandler(database=MockAccountTagDatabaseAdapter)


# Testa a instancia se ta ok
def test_account_tag_handler_istance(account_tag_handler: AccountTagHandler):
    assert isinstance(account_tag_handler, AccountTagHandler) == True
    assert issubclass(account_tag_handler._database, DatabaseAdapterInterface)


# Testa se está criando a conta normalmente
def test_account_tag_handler_create_account_tag(account_tag_handler: AccountTagHandler, account_tag_model: AccountTagModel):
    account_tag_handler.create_account_tag(account_tag=account_tag_model)
    assert isinstance(REGISTER[0], AccountTagModel) == True


# Testa se ta atualizando normal
def test_account_tag_handler_update_account_tag(account_tag_handler: AccountTagHandler, account_tag_model: AccountTagModel):
    new_name = "TEST NAME"
    new_created_at = datetime.now()
    new_user_id = uuid.uuid4()
    
    account_tag_model.id = REGISTER[0].id
    account_tag_model.name = new_name
    account_tag_model.created_at = new_created_at
    account_tag_model.user_id = new_user_id
    account_tag_handler.update_account_tag(id=account_tag_model.id, account_tag=account_tag_model)
    
    assert isinstance(REGISTER[0], AccountTagModel) == True
    assert REGISTER[0].name == new_name
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].user_id == new_user_id
    assert REGISTER[0].id == account_tag_model.id


# Testa se ta retornando a conta normalmente
def test_account_tag_handler_get_account_tag(account_tag_handler: AccountTagHandler):
    account_tag = account_tag_handler.get_account_tag(id=REGISTER[0].id)
    assert isinstance(account_tag, AccountTagModel) == True
    assert account_tag.id == REGISTER[0].id


# Testa se esta recebendo todas as contas registrada
def test_account_tag_handler_get_all_account_tags(account_tag_handler: AccountTagHandler):
    accounts = account_tag_handler.get_all_account_tags()
    assert len(accounts) == 1


# Testa se os changers estão funcionando
def test_account_tag_handler_changers_account_properts(account_tag_handler: AccountTagHandler):
    id = REGISTER[0].id
    new_name = "TEST NAME"
    new_created_at = datetime.now()
    new_user_id = uuid.uuid4()
    
    account_tag_handler.change_name(id=id, name=new_name)
    account_tag_handler.change_user_id(id=id, user_id=new_user_id)
    account_tag_handler.change_created_at(id=id, created_at=new_created_at)
    
    assert REGISTER[0].name == new_name
    assert REGISTER[0].user_id == new_user_id
    assert REGISTER[0].created_at == new_created_at


# Testa se o delete ta funcionando
def test_account_tag_handler_delete_account_tag(account_tag_handler: AccountTagHandler):
    account_tag_handler.delete_account_tag(id=REGISTER[0].id)
    assert len(REGISTER) == 0


# Testa o erro de tipo do database em propriedade
def test_account_tag_handler_database_type_error_01(account_tag_handler: AccountTagHandler):
    with pytest.raises(account_tag_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'value'"):
        account_tag_handler.database = "TESTE STRING TYPE"


# Testa o erro de tipo do database ao istanciar
def test_account_tag_handler_database_type_error_02():
    with pytest.raises(account_tag_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'databese'"):
        AccountTagHandler(database="TESTE STRING TYPE")


# Testa o erro de tipo ao criar conta
def test_account_tag_handler_unexpected_type_error_create_account_tag(account_tag_handler: AccountTagHandler):
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'account_tag'"):
        account_tag_handler.create_account_tag(account_tag="TESTE STRING TYPE")


# Testa o erro de tipo ao atualizar conta
def test_account_tag_handler_unexpected_type_error_update_account_tag(account_tag_handler: AccountTagHandler, account_tag_model: AccountTagModel):
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_tag_handler.update_account_tag(id="TESTE STRING TYPE", account_tag=account_tag_model)
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'account_tag'"):
        account_tag_handler.update_account_tag(id=uuid.uuid4(), account_tag="TESTE STRING TYPE")


# Testa o erro de tipo ao deletar conta
def test_account_tag_handler_unexpected_type_error_delete_account_tag(account_tag_handler: AccountTagHandler):
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_tag_handler.delete_account_tag(id="TESTE STRING TYPE")


# Testa o erro de tipo ao receber conta
def test_account_tag_handler_unexpected_type_error_get_account_tag(account_tag_handler: AccountTagHandler):
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_tag_handler.get_account_tag(id="TESTE STRING TYPE")


# Testa o erro de tipo ao mudar nome da conta
def test_account_tag_handler_unexpected_type_error_change_name(account_tag_handler: AccountTagHandler):
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_tag_handler.change_name(id="TESTE STRING TYPE", name="Nome")
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'name'"):
        account_tag_handler.change_name(id=uuid.uuid4(), name=1.0)


# Testa o erro de tipo ao mudar data de criação da conta
def test_account_tag_handler_unexpected_type_error_change_created_at(account_tag_handler: AccountTagHandler):
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_tag_handler.change_created_at(id="TESTE STRING TYPE", created_at=datetime.now())
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'created_at'"):
        account_tag_handler.change_created_at(id=uuid.uuid4(), created_at="TESTE STRING TYPE")


# Testa o erro de tipo no id ao mudar usuário da conta
def test_account_tag_handler_unexpected_type_error_change_user_id(account_tag_handler: AccountTagHandler):
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_tag_handler.change_user_id(id="TESTE STRING TYPE", user_id=uuid.uuid4())
    with pytest.raises(account_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'user_id'"):
        account_tag_handler.change_user_id(id=uuid.uuid4(), user_id="TESTE STRING TYPE")
