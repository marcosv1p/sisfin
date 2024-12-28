import pytest
import uuid

from datetime import datetime
from typing import Optional, List

from src.financial.models import TransactionCategoryModel
from src.financial.handlers import TransactionCategoryHandler
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.handler_errors import transaction_category_handler_error


REGISTER = []


class MockTransactionCategoryDatabaseAdapter(DatabaseAdapterInterface):
    _db = None
    @classmethod
    def insert(cls, transaction_category) -> None:
        REGISTER.append(transaction_category)
        return True
    
    @classmethod
    def update(cls, id, transaction_category) -> None:
        result = next((transaction_category for transaction_category in REGISTER if transaction_category.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
        REGISTER.insert(idx, transaction_category)
    
    @classmethod
    def delete(cls, id) -> None:
        result = next((transaction_category for transaction_category in REGISTER if transaction_category.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
    
    @classmethod
    def get(cls, id) -> Optional[TransactionCategoryModel]:
        return next((transaction_category for transaction_category in REGISTER if transaction_category.id == id), None)
    
    @classmethod
    def get_all(cls) -> List[TransactionCategoryModel]:
        return REGISTER


@pytest.fixture
def transaction_category_model():
    return TransactionCategoryModel(name="Minha Tag Teste", user_id=uuid.uuid4())


@pytest.fixture
def transaction_category_handler():
    return TransactionCategoryHandler(database=MockTransactionCategoryDatabaseAdapter)


# Testa a instancia se ta ok
def test_transaction_category_handler_istance(transaction_category_handler: TransactionCategoryHandler):
    assert isinstance(transaction_category_handler, TransactionCategoryHandler) == True
    assert issubclass(transaction_category_handler._database, DatabaseAdapterInterface)


# Testa se está criando a conta normalmente
def test_transaction_category_handler_create_transaction_category(transaction_category_handler: TransactionCategoryHandler, transaction_category_model: TransactionCategoryModel):
    transaction_category_handler.create_transaction_category(transaction_category=transaction_category_model)
    assert isinstance(REGISTER[0], TransactionCategoryModel) == True


# Testa se ta atualizando normal
def test_transaction_category_handler_update_transaction_category(transaction_category_handler: TransactionCategoryHandler, transaction_category_model: TransactionCategoryModel):
    new_name = "TEST NAME"
    new_created_at = datetime.now()
    new_user_id = uuid.uuid4()
    
    transaction_category_model.id = REGISTER[0].id
    transaction_category_model.name = new_name
    transaction_category_model.created_at = new_created_at
    transaction_category_model.user_id = new_user_id
    transaction_category_handler.update_transaction_category(id=transaction_category_model.id, transaction_category=transaction_category_model)
    
    assert isinstance(REGISTER[0], TransactionCategoryModel) == True
    assert REGISTER[0].name == new_name
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].user_id == new_user_id
    assert REGISTER[0].id == transaction_category_model.id


# Testa se ta retornando a conta normalmente
def test_transaction_category_handler_get_transaction_category(transaction_category_handler: TransactionCategoryHandler):
    transaction_category = transaction_category_handler.get_transaction_category(id=REGISTER[0].id)
    assert isinstance(transaction_category, TransactionCategoryModel) == True
    assert transaction_category.id == REGISTER[0].id


# Testa se esta recebendo todas as contas registrada
def test_transaction_category_handler_get_all_transaction_categoriess(transaction_category_handler: TransactionCategoryHandler):
    accounts = transaction_category_handler.get_all_transaction_categories()
    assert len(accounts) == 1


# Testa se os changers estão funcionando
def test_transaction_category_handler_changers_account_properts(transaction_category_handler: TransactionCategoryHandler):
    id = REGISTER[0].id
    new_name = "TEST NAME"
    new_created_at = datetime.now()
    new_user_id = uuid.uuid4()
    
    transaction_category_handler.change_name(id=id, name=new_name)
    transaction_category_handler.change_user_id(id=id, user_id=new_user_id)
    transaction_category_handler.change_created_at(id=id, created_at=new_created_at)
    
    assert REGISTER[0].name == new_name
    assert REGISTER[0].user_id == new_user_id
    assert REGISTER[0].created_at == new_created_at


# Testa se o delete ta funcionando
def test_transaction_category_handler_delete_transaction_category(transaction_category_handler: TransactionCategoryHandler):
    transaction_category_handler.delete_transaction_category(id=REGISTER[0].id)
    assert len(REGISTER) == 0


# Testa o erro de tipo do database em propriedade
def test_transaction_category_handler_database_type_error_01(transaction_category_handler: TransactionCategoryHandler):
    with pytest.raises(transaction_category_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'value'"):
        transaction_category_handler.database = "TESTE STRING TYPE"


# Testa o erro de tipo do database ao istanciar
def test_transaction_category_handler_database_type_error_02():
    with pytest.raises(transaction_category_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'databese'"):
        TransactionCategoryHandler(database="TESTE STRING TYPE")


# Testa o erro de tipo ao criar conta
def test_transaction_category_handler_unexpected_type_error_create_transaction_category(transaction_category_handler: TransactionCategoryHandler):
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'transaction_category'"):
        transaction_category_handler.create_transaction_category(transaction_category="TESTE STRING TYPE")


# Testa o erro de tipo ao atualizar conta
def test_transaction_category_handler_unexpected_type_error_update_transaction_category(transaction_category_handler: TransactionCategoryHandler, transaction_category_model: TransactionCategoryModel):
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_category_handler.update_transaction_category(id="TESTE STRING TYPE", transaction_category=transaction_category_model)
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'transaction_category'"):
        transaction_category_handler.update_transaction_category(id=uuid.uuid4(), transaction_category="TESTE STRING TYPE")


# Testa o erro de tipo ao deletar conta
def test_transaction_category_handler_unexpected_type_error_delete_transaction_category(transaction_category_handler: TransactionCategoryHandler):
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_category_handler.delete_transaction_category(id="TESTE STRING TYPE")


# Testa o erro de tipo ao receber conta
def test_transaction_category_handler_unexpected_type_error_get_transaction_category(transaction_category_handler: TransactionCategoryHandler):
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_category_handler.get_transaction_category(id="TESTE STRING TYPE")


# Testa o erro de tipo ao mudar nome da conta
def test_transaction_category_handler_unexpected_type_error_change_name(transaction_category_handler: TransactionCategoryHandler):
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_category_handler.change_name(id="TESTE STRING TYPE", name="Nome")
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'name'"):
        transaction_category_handler.change_name(id=uuid.uuid4(), name=1.0)


# Testa o erro de tipo ao mudar data de criação da conta
def test_transaction_category_handler_unexpected_type_error_change_created_at(transaction_category_handler: TransactionCategoryHandler):
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_category_handler.change_created_at(id="TESTE STRING TYPE", created_at=datetime.now())
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'created_at'"):
        transaction_category_handler.change_created_at(id=uuid.uuid4(), created_at="TESTE STRING TYPE")


# Testa o erro de tipo no id ao mudar usuário da conta
def test_transaction_category_handler_unexpected_type_error_change_user_id(transaction_category_handler: TransactionCategoryHandler):
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_category_handler.change_user_id(id="TESTE STRING TYPE", user_id=uuid.uuid4())
    with pytest.raises(transaction_category_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'user_id'"):
        transaction_category_handler.change_user_id(id=uuid.uuid4(), user_id="TESTE STRING TYPE")
