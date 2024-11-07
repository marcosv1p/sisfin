import pytest
from uuid import uuid4, UUID
from pydantic import ValidationError
from datetime import datetime
from decimal import Decimal
from src.financial import AccountModel


def test_account_model_creation():
    # Testa a criação de uma instância de AccountModel com dados válidos
    account = AccountModel(bank=uuid4(), name="Conta Padrão", description="Conta de uso geral", balance=Decimal("100.00"))
    assert isinstance(account.bank, UUID)
    assert account.name == "Conta Padrão"
    assert account.description == "Conta de uso geral"
    assert account.balance == Decimal("100.00")
    assert isinstance(account.account_id, UUID)
    assert isinstance(account.created_at, datetime)

def test_account_model_name_validation():
    # Testa restrições de caracteres e comprimento para o campo `name`
    
    # Nome vazio deve falhar
    with pytest.raises(ValidationError):
        AccountModel(bank=uuid4(), name="")

    # Nome com mais de 64 caracteres deve falhar
    with pytest.raises(ValidationError):
        AccountModel(bank=uuid4(), name="*" * 65)

    # Nome com caracteres válidos deve ser aceito
    account = AccountModel(bank=uuid4(), name="Conta Teste - Á é ç ó")
    assert account.name == "Conta Teste - Á é ç ó"

    # Nome com vírgula deve falhar, pois `name` não permite vírgulas
    with pytest.raises(ValidationError):
        AccountModel(bank=uuid4(), name="Conta, com vírgula")

def test_account_model_description_allows_comma():
    # Testa que `description` aceita vírgulas enquanto `name` não permite.
    account = AccountModel(bank=uuid4(), name="Conta Simples", description="Conta de exemplo, para teste")
    assert account.description == "Conta de exemplo, para teste"

def test_account_model_balance_precision():
    # Verifica se o `balance` aceita somente duas casas decimais
    account = AccountModel(bank=uuid4(), name="Conta Padrão", balance=Decimal("100.12"))
    assert account.balance == Decimal("100.12")

def test_account_model_update():
    # Cria uma instância de AccountModel e testa a atualização de alguns atributos
    account = AccountModel(bank=uuid4(), name="Conta Original", description="Descrição inicial", balance=Decimal("50.00"))

    # Define novos valores para atualizar
    updated_data = {
        "name": "Conta Atualizada",
        "description": "Descrição Atualizada, mais completa",
        "balance": Decimal("150.00")
    }

    # Realiza a atualização e verifica se os valores foram aplicados corretamente
    account.update(**updated_data)
    assert account.name == "Conta Atualizada"
    assert account.description == "Descrição Atualizada, mais completa"
    assert account.balance == Decimal("150.00")
    assert account.created_at  # `created_at` não deve mudar

def test_account_model_created_at_immutable():
    # Testa que o campo `created_at` não é atualizado durante o `update`
    account = AccountModel(bank=uuid4(), name="Conta Teste")
    original_created_at = account.created_at

    # Atualiza o banco, mas sem passar `created_at`
    account.update(name="Conta Atualizada")
    assert account.created_at == original_created_at  # `created_at` permanece o mesmo

def test_account_model_invalid_fields_ignored_in_update():
    # Testa que campos desconhecidos resultam em um erro de atualização
    account = AccountModel(bank=uuid4(), name="Conta Original")

    # Tenta atualizar usando um campo inexistente e verifica se ocorre um ValueError
    with pytest.raises(ValueError) as excinfo:
        account.update(name="Conta Atualizada", unknown_field="Valor Ignorado")
    assert "O atributo 'unknown_field' não existe na classe AccountModel" in str(excinfo.value)

def test_account_model_invalid_balance():
    # Testa que um valor inválido para `balance` gera erro de validação
    with pytest.raises(ValidationError):
        AccountModel(bank=uuid4(), name="Conta Simples", balance="not-a-valid-balance")

