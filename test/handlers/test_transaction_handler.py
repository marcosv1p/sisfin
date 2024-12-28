import pytest
import uuid

from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from random import randint

from src.financial.models import TransactionModel, TransactionTypes
from src.financial.handlers import TransactionHandler
from src.financial.interfaces import DatabaseAdapterInterface
from src.financial.exceptions.handler_errors import transaction_handler_error


REGISTER = []


class MockTransactionDatabaseAdapter(DatabaseAdapterInterface):
    _db = None
    @classmethod
    def insert(cls, transaction) -> None:
        REGISTER.append(transaction)
        return True
    
    @classmethod
    def update(cls, id, transaction) -> None:
        result = next((transaction for transaction in REGISTER if transaction.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
        REGISTER.insert(idx, transaction)
    
    @classmethod
    def delete(cls, id) -> None:
        result = next((transaction for transaction in REGISTER if transaction.id == id), None)
        idx = REGISTER.index(result)
        REGISTER.pop(idx)
    
    @classmethod
    def get(cls, id) -> Optional[TransactionModel]:
        return next((transaction for transaction in REGISTER if transaction.id == id), None)
    
    @classmethod
    def get_all(cls) -> List[TransactionModel]:
        return REGISTER


@pytest.fixture
def transaction_model():
    list_types = [TransactionTypes.ADJUST, TransactionTypes.EXPENSE, TransactionTypes.INCOME, TransactionTypes.EXPENSE]
    return TransactionModel(transaction_type=list_types[randint(0, 3)], category_id=uuid.uuid4(), account_id_destination=uuid.uuid4(), account_id_origin=uuid.uuid4(), user_id=uuid.uuid4())


@pytest.fixture
def transaction_handler():
    return TransactionHandler(database=MockTransactionDatabaseAdapter)


# Testa a instancia se ta ok
def test_transaction_handler_istance(transaction_handler: TransactionHandler):
    assert isinstance(transaction_handler, TransactionHandler) == True
    assert issubclass(transaction_handler._database, DatabaseAdapterInterface)


# Testa se está criando a transação normalmente
def test_transaction_handler_create_transaction(transaction_handler: TransactionHandler, transaction_model: TransactionModel):
    transaction_handler.create_transaction(transaction=transaction_model)
    assert isinstance(REGISTER[0], TransactionModel) == True


# Testa se ta atualizando normal
def test_transaction_handler_update_transaction(transaction_handler: TransactionHandler, transaction_model: TransactionModel):
    new_date = transaction_model.date
    new_description = "transaction_model.description"
    new_amount = Decimal("1000.00")
    new_transaction_type = transaction_model.transaction_type
    new_paid = False
    new_ignore = False
    new_visible = False
    new_category_id = transaction_model.category_id
    new_tag_id = transaction_model.tag_id
    new_account_id_origin = transaction_model.account_id_origin
    new_account_id_destination = transaction_model.account_id_destination
    new_created_at = transaction_model.created_at
    new_user_id = transaction_model.user_id
    
    transaction_model.id = REGISTER[0].id
    transaction_model.date = new_date
    transaction_model.description = new_description
    transaction_model.amount = new_amount
    transaction_model.transaction_type = new_transaction_type
    transaction_model.paid = new_paid
    transaction_model.ignore = new_ignore
    transaction_model.visible = new_visible
    transaction_model.category_id = new_category_id
    transaction_model.tag_id = new_tag_id
    transaction_model.account_id_origin = new_account_id_origin
    transaction_model.account_id_destination = new_account_id_destination
    transaction_model.created_at = new_created_at
    transaction_model.user_id = new_user_id
    
    transaction_handler.update_transaction(id=transaction_model.id, transaction=transaction_model)
    
    assert isinstance(REGISTER[0], TransactionModel) == True
    assert REGISTER[0].date == new_date
    assert REGISTER[0].description == new_description
    assert REGISTER[0].amount == new_amount
    assert REGISTER[0].transaction_type == new_transaction_type
    assert REGISTER[0].paid == new_paid
    assert REGISTER[0].ignore == new_ignore
    assert REGISTER[0].visible == new_visible
    assert REGISTER[0].category_id == new_category_id
    assert REGISTER[0].tag_id == new_tag_id
    assert REGISTER[0].account_id_origin == new_account_id_origin
    assert REGISTER[0].account_id_destination == new_account_id_destination
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].user_id == new_user_id
    assert REGISTER[0].id == transaction_model.id


# Testa se ta retornando a transação normalmente
def test_transaction_handler_get_transaction(transaction_handler: TransactionHandler):
    transaction = transaction_handler.get_transaction(id=REGISTER[0].id)
    assert isinstance(transaction, TransactionModel) == True
    assert transaction.id == REGISTER[0].id


# Testa se esta recebendo todas as transaçãos registrada
def test_transaction_handler_get_all_transactions(transaction_handler: TransactionHandler):
    accounts = transaction_handler.get_all_transactions()
    assert len(accounts) == 1


# Testa se os changers estão funcionando
def test_transaction_handler_changers_account_properts(transaction_handler: TransactionHandler, transaction_model: TransactionModel):
    id = REGISTER[0].id
    new_date = transaction_model.date
    new_description = "transaction_model.description"
    new_amount = Decimal("1000.00")
    new_transaction_type = transaction_model.transaction_type
    new_paid = False
    new_ignore = False
    new_visible = False
    new_category_id = transaction_model.category_id
    new_tag_id = transaction_model.tag_id
    new_account_id_origin = transaction_model.account_id_origin
    new_account_id_destination = transaction_model.account_id_destination
    new_created_at = transaction_model.created_at
    new_user_id = transaction_model.user_id
    
    transaction_handler.change_date(id=id, date=new_date)
    transaction_handler.change_description(id=id, description=new_description)
    transaction_handler.change_amount(id=id, amount=new_amount)
    transaction_handler.change_transaction_type(id=id, transaction_type=new_transaction_type)
    transaction_handler.change_paid(id=id, paid=new_paid)
    transaction_handler.change_ignore(id=id, ignore=new_ignore)
    transaction_handler.change_visible(id=id, visible=new_visible)
    transaction_handler.change_category_id(id=id, category_id=new_category_id)
    transaction_handler.change_tag_id(id=id, tag_id=new_tag_id)
    transaction_handler.change_account_id_origin(id=id, account_id_origin=new_account_id_origin)
    transaction_handler.change_account_id_destination(id=id, account_id_destination=new_account_id_destination)
    transaction_handler.change_created_at(id=id, created_at=new_created_at)
    transaction_handler.change_user_id(id=id, user_id=new_user_id)
    
    assert REGISTER[0].id == id
    assert REGISTER[0].date == new_date
    assert REGISTER[0].description == new_description
    assert REGISTER[0].amount == new_amount
    assert REGISTER[0].transaction_type == new_transaction_type
    assert REGISTER[0].paid == new_paid
    assert REGISTER[0].ignore == new_ignore
    assert REGISTER[0].visible == new_visible
    assert REGISTER[0].category_id == new_category_id
    assert REGISTER[0].tag_id == new_tag_id
    assert REGISTER[0].account_id_origin == new_account_id_origin
    assert REGISTER[0].account_id_destination == new_account_id_destination
    assert REGISTER[0].created_at == new_created_at
    assert REGISTER[0].user_id == new_user_id


# Testa se o delete ta funcionando
def test_transaction_handler_delete_transaction(transaction_handler: TransactionHandler):
    transaction_handler.delete_transaction(id=REGISTER[0].id)
    assert len(REGISTER) == 0


# Testa o erro de tipo do database em propriedade
def test_transaction_handler_database_type_error_01(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'value'"):
        transaction_handler.database = "TESTE STRING TYPE"


# Testa o erro de tipo do database ao istanciar
def test_transaction_handler_database_type_error_02():
    with pytest.raises(transaction_handler_error.UnexpectedDatabaseTypeError, match="Tipo inesperado do argumento 'databese'"):
        TransactionHandler(database="TESTE STRING TYPE")


# Testa o erro de tipo ao criar transação
def test_transaction_handler_unexpected_type_error_create_transaction(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'transaction'"):
        transaction_handler.create_transaction(transaction="TESTE STRING TYPE")


# Testa o erro de tipo ao atualizar transação
def test_transaction_handler_unexpected_type_error_update_transaction(transaction_handler: TransactionHandler, transaction_model: TransactionModel):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.update_transaction(id="TESTE STRING TYPE", transaction=transaction_model)
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'transaction'"):
        transaction_handler.update_transaction(id=uuid.uuid4(), transaction="TESTE STRING TYPE")


# Testa o erro de tipo ao deletar transação
def test_transaction_handler_unexpected_type_error_delete_transaction(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.delete_transaction(id="TESTE STRING TYPE")


# Testa o erro de tipo ao receber transação
def test_transaction_handler_unexpected_type_error_get_transaction(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.get_transaction(id="TESTE STRING TYPE")


# Testa o erro de tipo ao mudar data da transação
def test_transaction_handler_unexpected_type_error_change_date(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_date(id="TESTE STRING TYPE", date=datetime.now())
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'date'"):
        transaction_handler.change_date(id=uuid.uuid4(), date=1.0)


# Testa o erro de tipo ao mudar descrição da transação
def test_transaction_handler_unexpected_type_error_change_description(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_description(id="TESTE STRING TYPE", description="BLA BLA")
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'description'"):
        transaction_handler.change_description(id=uuid.uuid4(), description=1.0)


# Testa o erro de tipo ao mudar valor da transação
def test_transaction_handler_unexpected_type_error_change_amount(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_amount(id="TESTE STRING TYPE", amount=Decimal("1.0"))
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'amount'"):
        transaction_handler.change_amount(id=uuid.uuid4(), amount=1.0)


# Testa o erro de tipo ao mudar tipo da transação
def test_transaction_handler_unexpected_type_error_change_transaction_type(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_transaction_type(id="TESTE STRING TYPE", transaction_type=TransactionTypes.EXPENSE)
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'transaction_type'"):
        transaction_handler.change_transaction_type(id=uuid.uuid4(), transaction_type=1.0)


# Testa o erro de tipo ao mudar pago da transação
def test_transaction_handler_unexpected_type_error_change_paid(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_paid(id="TESTE STRING TYPE", paid=True)
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'paid'"):
        transaction_handler.change_paid(id=uuid.uuid4(), paid=1.0)


# Testa o erro de tipo ao mudar ignorar da transação
def test_transaction_handler_unexpected_type_error_change_ignore(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_ignore(id="TESTE STRING TYPE", ignore=True)
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'ignore'"):
        transaction_handler.change_ignore(id=uuid.uuid4(), ignore=1.0)


# Testa o erro de tipo ao mudar visibilidade da transação
def test_transaction_handler_unexpected_type_error_change_visible(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_visible(id="TESTE STRING TYPE", visible=True)
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'visible'"):
        transaction_handler.change_visible(id=uuid.uuid4(), visible=1.0)


# Testa o erro de tipo ao mudar categoria da transação
def test_transaction_handler_unexpected_type_error_change_category_id(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_category_id(id="TESTE STRING TYPE", category_id=uuid.uuid4())
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'category_id'"):
        transaction_handler.change_category_id(id=uuid.uuid4(), category_id=1.0)


# Testa o erro de tipo ao mudar tag da transação
def test_transaction_handler_unexpected_type_error_change_tag_id(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_tag_id(id="TESTE STRING TYPE", tag_id=uuid.uuid4())
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'tag_id'"):
        transaction_handler.change_tag_id(id=uuid.uuid4(), tag_id=1.0)


# Testa o erro de tipo ao mudar origem da transação
def test_transaction_handler_unexpected_type_error_change_account_id_origin(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_account_id_origin(id="TESTE STRING TYPE", account_id_origin=uuid.uuid4())
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'account_id_origin'"):
        transaction_handler.change_account_id_origin(id=uuid.uuid4(), account_id_origin="TESTE STRING TYPE")


# Testa o erro de tipo ao mudar destino da transação
def test_transaction_handler_unexpected_type_error_change_account_id_destination(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_account_id_destination(id="TESTE STRING TYPE", account_id_destination=uuid.uuid4())
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'account_id_destination'"):
        transaction_handler.change_account_id_destination(id=uuid.uuid4(), account_id_destination="TESTE STRING TYPE")


# Testa o erro de tipo ao mudar data de criação da transação
def test_transaction_handler_unexpected_type_error_change_created_at(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_created_at(id="TESTE STRING TYPE", created_at=datetime.now())
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'created_at'"):
        transaction_handler.change_created_at(id=uuid.uuid4(), created_at="TESTE STRING TYPE")


# Testa o erro de tipo no id ao mudar usuário da transação
def test_transaction_handler_unexpected_type_error_change_user_id(transaction_handler: TransactionHandler):
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'id'"):
        transaction_handler.change_user_id(id="TESTE STRING TYPE", user_id=uuid.uuid4())
    with pytest.raises(transaction_handler_error.UnexpectedArgumentTypeError, match="Tipo inesperado do argumento 'user_id'"):
        transaction_handler.change_user_id(id=uuid.uuid4(), user_id="TESTE STRING TYPE")
