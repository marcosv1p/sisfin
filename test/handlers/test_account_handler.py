import pytest
import uuid

from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from src.financial.models import AccountModel
from src.financial.handlers import AccountHandler
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.handler_errors import account_handler_error


REGISTER = []


class MockAccountDatabaseAdapter(DatabaseAdapterInterface):
    _db = None
    @classmethod
    def insert(cls, account) -> None:
        REGISTER.append(account)
        return True
    
    @classmethod
    def update(cls, id, account) -> None:
        result = next((account for account in REGISTER if account.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
        REGISTER.insert(idx, account)
    
    @classmethod
    def delete(cls, id) -> None:
        result = next((account for account in REGISTER if account.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
    
    @classmethod
    def get(cls, id) -> Optional[AccountModel]:
        return next((account for account in REGISTER if account.id == id), None)
    
    @classmethod
    def get_all(cls) -> List[AccountModel]:
        return REGISTER


@pytest.fixture
def account_model():
    return AccountModel(user_id=uuid.uuid4())


@pytest.fixture
def account_handler():
    return AccountHandler(database=MockAccountDatabaseAdapter)


# Testa a instancia se ta ok
def test_account_handler_istance(account_handler: AccountHandler):
    assert isinstance(account_handler, AccountHandler) == True
    assert issubclass(account_handler._database, DatabaseAdapterInterface)


# Testa se está criando a conta normalmente
def test_account_handler_create_account(account_handler: AccountHandler, account_model: AccountModel):
    account_handler.create_account(account=account_model)
    assert isinstance(REGISTER[0], AccountModel) == True


# Testa se ta atualizando normal
def test_account_handler_update_account(account_handler: AccountHandler, account_model: AccountModel):
    new_name = "TEST NAME"
    new_description = "TEST DESCRIPTION"
    new_tag_id = uuid.uuid4()
    new_balance = Decimal("999.99")
    new_created_at = datetime.now()
    new_user_id = uuid.uuid4()
    
    account_model.id = REGISTER[0].id
    account_model.name = new_name
    account_model.description = new_description
    account_model.tag_id = new_tag_id
    account_model.balance = new_balance
    account_model.created_at = new_created_at
    account_model.user_id = new_user_id
    account_handler.update_account(id=account_model.id, account=account_model)
    
    assert isinstance(REGISTER[0], AccountModel) == True
    assert REGISTER[0].name == new_name
    assert REGISTER[0].description == new_description
    assert REGISTER[0].tag_id == new_tag_id
    assert REGISTER[0].balance == new_balance
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].user_id == new_user_id
    assert REGISTER[0].id == account_model.id


# Testa se ta retornando a conta normalmente
def test_account_handler_get_account(account_handler: AccountHandler):
    account = account_handler.get_account(id=REGISTER[0].id)
    assert isinstance(account, AccountModel) == True
    assert account.id == REGISTER[0].id


# Testa se esta recebendo todas as contas registrada
def test_account_handler_get_all_account(account_handler: AccountHandler):
    accounts = account_handler.get_all_accounts()
    assert len(accounts) == 1


# Testa se os changers estão funcionando
def test_account_handler_changers_account_properts(account_handler: AccountHandler, account_model: AccountModel):
    id = REGISTER[0].id
    new_name = "TEST NAME"
    new_description = "TEST DESCRIPTION"
    new_tag_id = uuid.uuid4()
    new_balance = Decimal("999.99")
    new_created_at = datetime.now()
    new_user_id = uuid.uuid4()
    
    account_handler.change_name(id=id, name=new_name)
    account_handler.change_description(id=id, description=new_description)
    account_handler.change_balance(id=id, balance=new_balance)
    account_handler.change_tag_id(id=id, tag_id=new_tag_id)
    account_handler.change_user_id(id=id, user_id=new_user_id)
    account_handler.change_created_at(id=id, created_at=new_created_at)
    
    assert REGISTER[0].name == new_name
    assert REGISTER[0].description == new_description
    assert REGISTER[0].balance == new_balance
    assert REGISTER[0].tag_id == new_tag_id
    assert REGISTER[0].user_id == new_user_id
    assert REGISTER[0].created_at == new_created_at


# Teste de adição de valor ao saldo
def test_account_handler_added_balance(account_handler: AccountHandler):
    old_balance = REGISTER[0].balance
    new_balance = old_balance + Decimal("1000.00")
    account_handler.added_balance(id=REGISTER[0].id, amount=Decimal("1000.00"))
    assert REGISTER[0].balance == new_balance


# Teste de retirada de valor do saldo
def test_account_handler_subtract_balance(account_handler: AccountHandler):
    old_balance = REGISTER[0].balance
    new_balance = old_balance - Decimal("1000.00")
    account_handler.subtract_balance(id=REGISTER[0].id, amount=Decimal("1000.00"))
    assert REGISTER[0].balance == new_balance


# Testa se o delete ta funcionando
def test_account_handler_delete_account(account_handler: AccountHandler):
    account_handler.delete_account(id=REGISTER[0].id)
    assert len(REGISTER) == 0


# Testa o erro de tipo do database em propriedade
def test_account_handler_database_type_error_01(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'value'"):
        account_handler.database = "TESTE STRING TYPE"


# Testa o erro de tipo do database ao istanciar
def test_account_handler_database_type_error_02():
    with pytest.raises(account_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'databese'"):
        AccountHandler(database="TESTE STRING TYPE")


# Testa o erro de tipo ao adicionar saldo
def test_account_handler_unexpected_type_error_added_balance(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.added_balance(id="TESTE STRING TYPE", amount=Decimal("100.00"))
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'amount'"):
        account_handler.added_balance(id=uuid.uuid4(), amount="TESTE STRING TYPE")


# Testa o erro de tipo ao subtrair saldo
def test_account_handler_unexpected_type_error_subtract_balance(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.subtract_balance(id="TESTE STRING TYPE", amount=Decimal("100.00"))
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'amount'"):
        account_handler.subtract_balance(id=uuid.uuid4(), amount="TESTE STRING TYPE")


# Testa o erro de tipo ao criar conta
def test_account_handler_unexpected_type_error_create_account(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'account'"):
        account_handler.create_account(account="TESTE STRING TYPE")


# Testa o erro de tipo ao atualizar conta
def test_account_handler_unexpected_type_error_update_account(account_handler: AccountHandler, account_model: AccountModel):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.update_account(id="TESTE STRING TYPE", account=account_model)
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'account'"):
        account_handler.update_account(id=uuid.uuid4(), account="TESTE STRING TYPE")


# Testa o erro de tipo ao deletar conta
def test_account_handler_unexpected_type_error_delete_account(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.delete_account(id="TESTE STRING TYPE")


# Testa o erro de tipo ao receber conta
def test_account_handler_unexpected_type_error_get_account(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.get_account(id="TESTE STRING TYPE")


# Testa o erro de tipo ao mudar saldo da conta
def test_account_handler_unexpected_type_error_change_balance(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.change_balance(id="TESTE STRING TYPE", balance=Decimal("1.00"))
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'balance'"):
        account_handler.change_balance(id=uuid.uuid4(), balance="TESTE STRING TYPE")


# Testa o erro de tipo ao mudar nome da conta
def test_account_handler_unexpected_type_error_change_name(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.change_name(id="TESTE STRING TYPE", name="Nome")
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'name'"):
        account_handler.change_name(id=uuid.uuid4(), name=1.0)


# Testa o erro de tipo ao mudar descrição da conta
def test_account_handler_unexpected_type_error_change_description(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.change_description(id="TESTE STRING TYPE", description="Uma descrição")
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'description'"):
        account_handler.change_description(id=uuid.uuid4(), description=1.0)


# Testa o erro de tipo ao mudar tag da conta
def test_account_handler_unexpected_type_error_change_tag_id(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.change_tag_id(id="TESTE STRING TYPE", tag_id=uuid.uuid4())
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'tag_id'"):
        account_handler.change_tag_id(id=uuid.uuid4(), tag_id="TESTE STRING TYPE")


# Testa o erro de tipo ao mudar data de criação da conta
def test_account_handler_unexpected_type_error_change_created_at(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.change_created_at(id="TESTE STRING TYPE", created_at=datetime.now())
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'created_at'"):
        account_handler.change_created_at(id=uuid.uuid4(), created_at="TESTE STRING TYPE")


# Testa o erro de tipo no id ao mudar usuário da conta
def test_account_handler_unexpected_type_error_change_user_id(account_handler: AccountHandler):
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        account_handler.change_user_id(id="TESTE STRING TYPE", user_id=uuid.uuid4())
    with pytest.raises(account_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'user_id'"):
        account_handler.change_user_id(id=uuid.uuid4(), user_id="TESTE STRING TYPE")
