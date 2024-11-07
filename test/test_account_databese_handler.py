import pytest
from uuid import uuid4, UUID
from decimal import Decimal
from datetime import datetime
from src.financial.account import AccountModel
from src.financial import AccountDatabaseHandler

# Fixtures para preparar contas
@pytest.fixture
def account_data():
    return AccountModel(
        account_id=uuid4(),
        bank=uuid4(),
        name="Conta Teste",
        description="Descrição de teste",
        balance=Decimal("1000.00"),
        created_at=datetime.now()
    )

@pytest.fixture
def updated_account_data():
    return AccountModel(
        account_id=uuid4(),
        bank=uuid4(),
        name="Conta Atualizada",
        description="Descrição atualizada",
        balance=Decimal("2000.00"),
        created_at=datetime.now()
    )

# Testes de inserção
def test_insert_account(account_data):
    # Insere a conta no banco de dados
    AccountDatabaseHandler.insert(account_data)

    # Recupera a conta do banco de dados
    retrieved_account = AccountDatabaseHandler.get(account_data.account_id)

    assert retrieved_account is not None
    assert retrieved_account.account_id == account_data.account_id
    assert retrieved_account.name == account_data.name
    assert retrieved_account.balance == account_data.balance

# Testes de atualização
def test_update_account(account_data, updated_account_data):
    # Insere a conta original
    AccountDatabaseHandler.insert(account_data)

    # Atualiza os dados da conta
    AccountDatabaseHandler.update(account_data.account_id, updated_account_data)

    # Recupera a conta atualizada com o novo account_id
    updated_account = AccountDatabaseHandler.get(updated_account_data.account_id)

    # Verifica se a conta foi atualizada corretamente
    assert updated_account is not None
    assert updated_account.name == updated_account_data.name
    assert updated_account.balance == updated_account_data.balance
    assert updated_account.description == updated_account_data.description
    assert updated_account.bank == updated_account_data.bank

# Teste de exclusão
def test_delete_account(account_data):
    # Insere a conta no banco de dados
    AccountDatabaseHandler.insert(account_data)

    # Deleta a conta
    AccountDatabaseHandler.delete(account_data.account_id)

    # Tenta recuperar a conta, que deve ser None
    deleted_account = AccountDatabaseHandler.get(account_data.account_id)

    assert deleted_account is None

# Teste de recuperação de todas as contas
def test_get_all_accounts(account_data, updated_account_data):
    # Insere as contas no banco de dados
    AccountDatabaseHandler.insert(account_data)
    AccountDatabaseHandler.insert(updated_account_data)

    # Recupera todas as contas
    all_accounts = AccountDatabaseHandler.get_all()

    assert len(all_accounts) >= 2  # Deve retornar pelo menos 2 contas
    assert any(account.account_id == account_data.account_id for account in all_accounts)
    assert any(account.account_id == updated_account_data.account_id for account in all_accounts)

# Teste de conta não encontrada ao tentar atualizar
def test_update_account_not_found():
    invalid_account = AccountModel(
        account_id=uuid4(),  # Gerando um UUID para conta inexistente
        bank=UUID('7d77ad17-ded4-47dc-8ed7-8cccaf651511'),  # Um UUID válido para o banco
        name="Inexistente",
        description="Conta inexistente",
        balance=Decimal("500.00"),
        created_at=datetime.now()
    )
    
    # Espera-se que o erro seja lançado porque a conta não existe
    with pytest.raises(ValueError, match="Conta bancária não encontrada."):
        AccountDatabaseHandler.update(uuid4(), invalid_account)

# Teste de recuperação de conta não encontrada
def test_get_account_not_found():
    account = AccountDatabaseHandler.get(uuid4())
    assert account is None
