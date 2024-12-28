import pytest
import uuid

from datetime import datetime
from typing import Optional, List

from src.financial.models import TransactionTagModel
from src.financial.handlers import TransactionTagHandler
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.handler_errors import transaction_tag_handler_error


REGISTER = []


class MockTransactionTagDatabaseAdapter(DatabaseAdapterInterface):
    _db = None
    @classmethod
    def insert(cls, transaction_tag) -> None:
        REGISTER.append(transaction_tag)
        return True
    
    @classmethod
    def update(cls, id, transaction_tag) -> None:
        result = next((transaction_tag for transaction_tag in REGISTER if transaction_tag.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
        REGISTER.insert(idx, transaction_tag)
    
    @classmethod
    def delete(cls, id) -> None:
        result = next((transaction_tag for transaction_tag in REGISTER if transaction_tag.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
    
    @classmethod
    def get(cls, id) -> Optional[TransactionTagModel]:
        return next((transaction_tag for transaction_tag in REGISTER if transaction_tag.id == id), None)
    
    @classmethod
    def get_all(cls) -> List[TransactionTagModel]:
        return REGISTER


@pytest.fixture
def transaction_tag_model():
    return TransactionTagModel(name="Minha Tag Teste", user_id=uuid.uuid4())


@pytest.fixture
def transaction_tag_handler():
    return TransactionTagHandler(database=MockTransactionTagDatabaseAdapter)


# Testa a instancia se ta ok
def test_transaction_tag_handler_istance(transaction_tag_handler: TransactionTagHandler):
    assert isinstance(transaction_tag_handler, TransactionTagHandler) == True
    assert issubclass(transaction_tag_handler._database, DatabaseAdapterInterface)


# Testa se está criando a conta normalmente
def test_transaction_tag_handler_create_transaction_tag(transaction_tag_handler: TransactionTagHandler, transaction_tag_model: TransactionTagModel):
    transaction_tag_handler.create_transaction_tag(transaction_tag=transaction_tag_model)
    assert isinstance(REGISTER[0], TransactionTagModel) == True


# Testa se ta atualizando normal
def test_transaction_tag_handler_update_transaction_tag(transaction_tag_handler: TransactionTagHandler, transaction_tag_model: TransactionTagModel):
    new_name = "TEST NAME"
    new_created_at = datetime.now()
    new_user_id = uuid.uuid4()
    
    transaction_tag_model.id = REGISTER[0].id
    transaction_tag_model.name = new_name
    transaction_tag_model.created_at = new_created_at
    transaction_tag_model.user_id = new_user_id
    transaction_tag_handler.update_transaction_tag(id=transaction_tag_model.id, transaction_tag=transaction_tag_model)
    
    assert isinstance(REGISTER[0], TransactionTagModel) == True
    assert REGISTER[0].name == new_name
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].user_id == new_user_id
    assert REGISTER[0].id == transaction_tag_model.id


# Testa se ta retornando a conta normalmente
def test_transaction_tag_handler_get_transaction_tag(transaction_tag_handler: TransactionTagHandler):
    transaction_tag = transaction_tag_handler.get_transaction_tag(id=REGISTER[0].id)
    assert isinstance(transaction_tag, TransactionTagModel) == True
    assert transaction_tag.id == REGISTER[0].id


# Testa se esta recebendo todas as contas registrada
def test_transaction_tag_handler_get_all_transaction_tags(transaction_tag_handler: TransactionTagHandler):
    accounts = transaction_tag_handler.get_all_transaction_tags()
    assert len(accounts) == 1


# Testa se os changers estão funcionando
def test_transaction_tag_handler_changers_account_properts(transaction_tag_handler: TransactionTagHandler):
    id = REGISTER[0].id
    new_name = "TEST NAME"
    new_created_at = datetime.now()
    new_user_id = uuid.uuid4()
    
    transaction_tag_handler.change_name(id=id, name=new_name)
    transaction_tag_handler.change_user_id(id=id, user_id=new_user_id)
    transaction_tag_handler.change_created_at(id=id, created_at=new_created_at)
    
    assert REGISTER[0].name == new_name
    assert REGISTER[0].user_id == new_user_id
    assert REGISTER[0].created_at == new_created_at


# Testa se o delete ta funcionando
def test_transaction_tag_handler_delete_transaction_tag(transaction_tag_handler: TransactionTagHandler):
    transaction_tag_handler.delete_transaction_tag(id=REGISTER[0].id)
    assert len(REGISTER) == 0


# Testa o erro de tipo do database em propriedade
def test_transaction_tag_handler_database_type_error_01(transaction_tag_handler: TransactionTagHandler):
    with pytest.raises(transaction_tag_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'value'"):
        transaction_tag_handler.database = "TESTE STRING TYPE"


# Testa o erro de tipo do database ao istanciar
def test_transaction_tag_handler_database_type_error_02():
    with pytest.raises(transaction_tag_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'databese'"):
        TransactionTagHandler(database="TESTE STRING TYPE")


# Testa o erro de tipo ao criar conta
def test_transaction_tag_handler_unexpected_type_error_create_transaction_tag(transaction_tag_handler: TransactionTagHandler):
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'transaction_tag'"):
        transaction_tag_handler.create_transaction_tag(transaction_tag="TESTE STRING TYPE")


# Testa o erro de tipo ao atualizar conta
def test_transaction_tag_handler_unexpected_type_error_update_transaction_tag(transaction_tag_handler: TransactionTagHandler, transaction_tag_model: TransactionTagModel):
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_tag_handler.update_transaction_tag(id="TESTE STRING TYPE", transaction_tag=transaction_tag_model)
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'transaction_tag'"):
        transaction_tag_handler.update_transaction_tag(id=uuid.uuid4(), transaction_tag="TESTE STRING TYPE")


# Testa o erro de tipo ao deletar conta
def test_transaction_tag_handler_unexpected_type_error_delete_transaction_tag(transaction_tag_handler: TransactionTagHandler):
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_tag_handler.delete_transaction_tag(id="TESTE STRING TYPE")


# Testa o erro de tipo ao receber conta
def test_transaction_tag_handler_unexpected_type_error_get_transaction_tag(transaction_tag_handler: TransactionTagHandler):
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_tag_handler.get_transaction_tag(id="TESTE STRING TYPE")


# Testa o erro de tipo ao mudar nome da conta
def test_transaction_tag_handler_unexpected_type_error_change_name(transaction_tag_handler: TransactionTagHandler):
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_tag_handler.change_name(id="TESTE STRING TYPE", name="Nome")
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'name'"):
        transaction_tag_handler.change_name(id=uuid.uuid4(), name=1.0)


# Testa o erro de tipo ao mudar data de criação da conta
def test_transaction_tag_handler_unexpected_type_error_change_created_at(transaction_tag_handler: TransactionTagHandler):
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_tag_handler.change_created_at(id="TESTE STRING TYPE", created_at=datetime.now())
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'created_at'"):
        transaction_tag_handler.change_created_at(id=uuid.uuid4(), created_at="TESTE STRING TYPE")


# Testa o erro de tipo no id ao mudar usuário da conta
def test_transaction_tag_handler_unexpected_type_error_change_user_id(transaction_tag_handler: TransactionTagHandler):
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_tag_handler.change_user_id(id="TESTE STRING TYPE", user_id=uuid.uuid4())
    with pytest.raises(transaction_tag_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'user_id'"):
        transaction_tag_handler.change_user_id(id=uuid.uuid4(), user_id="TESTE STRING TYPE")
