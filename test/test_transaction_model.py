import pytest
from decimal import Decimal
from uuid import uuid4, UUID
from datetime import datetime
from pydantic import ValidationError
from src.financial import AccountModel, TransactionModel, TransactionsTypes


def test_transaction_model_creation():
    # Testa a criação de uma instância de TransactionModel com dados válidos
    destination_account = AccountModel(bank=uuid4(), name="Conta Destino", balance=Decimal("100.00"))
    transaction = TransactionModel(
        value=Decimal("50.00"),
        transaction_type=TransactionsTypes.DEPOSIT,
        destination=destination_account,
    )

    assert isinstance(transaction.transaction_id, UUID)
    assert isinstance(transaction.created_at, datetime)
    assert transaction.value == Decimal("50.00")
    assert transaction.transaction_type == TransactionsTypes.DEPOSIT
    assert transaction.destination == destination_account
    assert transaction.status is False  # Transação ainda não foi executada

def test_transaction_model_description_validation():
    # Testa que a descrição aceita caracteres permitidos e respeita o limite de comprimento

    # Descrição com caracteres válidos e dentro do limite
    transaction = TransactionModel(
        value=Decimal("20.00"),
        transaction_type=TransactionsTypes.WITHDRAW,
        destination=AccountModel(bank=uuid4(), name="Conta Teste"),
        description="Transação de teste - Á, é, ç"
    )
    assert transaction.description == "Transação de teste - Á, é, ç"

    # Descrição com vírgula é aceita
    transaction = TransactionModel(
        value=Decimal("30.00"),
        transaction_type=TransactionsTypes.DEPOSIT,
        destination=AccountModel(bank=uuid4(), name="Conta Teste"),
        description="Depósito, urgente"
    )
    assert transaction.description == "Depósito, urgente"

    # Descrição que ultrapassa 255 caracteres deve falhar
    with pytest.raises(ValidationError):
        TransactionModel(
            value=Decimal("10.00"),
            transaction_type=TransactionsTypes.DEPOSIT,
            destination=AccountModel(bank=uuid4(), name="Conta Teste"),
            description="A" * 256
        )

def test_transaction_execute_deposit():
    # Testa a execução de um depósito
    account = AccountModel(bank=uuid4(), name="Conta Destino", balance=Decimal("100.00"))
    transaction = TransactionModel(
        value=Decimal("50.00"),
        transaction_type=TransactionsTypes.DEPOSIT,
        destination=account
    )
    transaction.execute()
    assert transaction.status is True
    assert account.balance == Decimal("150.00")  # Saldo atualizado com o depósito

def test_transaction_execute_withdraw():
    # Testa a execução de um saque
    account = AccountModel(bank=uuid4(), name="Conta Destino", balance=Decimal("100.00"))
    transaction = TransactionModel(
        value=Decimal("30.00"),
        transaction_type=TransactionsTypes.WITHDRAW,
        destination=account
    )
    transaction.execute()
    assert transaction.status is True
    assert account.balance == Decimal("70.00")  # Saldo atualizado com o saque

def test_transaction_execute_transfer():
    # Testa a execução de uma transferência entre duas contas
    origin_account = AccountModel(bank=uuid4(), name="Conta Origem", balance=Decimal("200.00"))
    destination_account = AccountModel(bank=uuid4(), name="Conta Destino", balance=Decimal("100.00"))
    transaction = TransactionModel(
        value=Decimal("50.00"),
        transaction_type=TransactionsTypes.TRANSFER,
        origin=origin_account,
        destination=destination_account
    )
    transaction.execute()
    assert transaction.status is True
    assert origin_account.balance == Decimal("150.00")  # Deduzido do saldo da conta de origem
    assert destination_account.balance == Decimal("150.00")  # Adicionado ao saldo da conta de destino

def test_transaction_execute_without_origin_for_transfer():
    # Testa erro ao tentar executar uma transferência sem conta de origem
    destination_account = AccountModel(bank=uuid4(), name="Conta Destino", balance=Decimal("100.00"))
    transaction = TransactionModel(
        value=Decimal("50.00"),
        transaction_type=TransactionsTypes.TRANSFER,
        destination=destination_account
    )
    with pytest.raises(ValueError, match="Origin account is required for transfer"):
        transaction.execute()

def test_transaction_undo_execute_deposit():
    # Testa a reversão de um depósito
    account = AccountModel(bank=uuid4(), name="Conta Destino", balance=Decimal("100.00"))
    transaction = TransactionModel(
        value=Decimal("50.00"),
        transaction_type=TransactionsTypes.DEPOSIT,
        destination=account
    )
    transaction.execute()
    transaction.undo_execute()
    assert transaction.status is False
    assert account.balance == Decimal("100.00")  # Saldo revertido ao valor original

def test_transaction_undo_execute_withdraw():
    # Testa a reversão de um saque
    account = AccountModel(bank=uuid4(), name="Conta Destino", balance=Decimal("100.00"))
    transaction = TransactionModel(
        value=Decimal("30.00"),
        transaction_type=TransactionsTypes.WITHDRAW,
        destination=account
    )
    transaction.execute()
    transaction.undo_execute()
    assert transaction.status is False
    assert account.balance == Decimal("100.00")  # Saldo revertido ao valor original

def test_transaction_undo_execute_transfer():
    # Testa a reversão de uma transferência
    origin_account = AccountModel(bank=uuid4(), name="Conta Origem", balance=Decimal("200.00"))
    destination_account = AccountModel(bank=uuid4(), name="Conta Destino", balance=Decimal("100.00"))
    transaction = TransactionModel(
        value=Decimal("50.00"),
        transaction_type=TransactionsTypes.TRANSFER,
        origin=origin_account,
        destination=destination_account
    )
    transaction.execute()
    transaction.undo_execute()
    assert transaction.status is False
    assert origin_account.balance == Decimal("200.00")  # Saldo revertido ao valor original
    assert destination_account.balance == Decimal("100.00")  # Saldo revertido ao valor original

def test_transaction_invalid_type():
    # Testa erro ao tentar criar uma transação com tipo inválido
    account = AccountModel(bank=uuid4(), name="Conta Destino", balance=Decimal("100.00"))
    with pytest.raises(ValidationError, match="Input should be 'deposit', 'withdraw' or 'transfer'"):
        TransactionModel(
            value=Decimal("50.00"),
            transaction_type="INVALID",  # Tipo inválido
            destination=account
        )
