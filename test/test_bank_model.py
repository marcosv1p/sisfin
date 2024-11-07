import pytest
from uuid import UUID
from datetime import datetime
from pydantic import ValidationError
from src.financial import BankModel


def test_bank_model_creation():
    # Testa a criação de uma instância de BankModel com dados válidos
    bank = BankModel(name="Banco Simples", description="Banco de confiança", url_image="https://example.com/logo.png")
    assert bank.name == "Banco Simples"
    assert bank.description == "Banco de confiança"
    assert str(bank.url_image) == "https://example.com/logo.png"
    assert isinstance(bank.bank_id, UUID)
    assert isinstance(bank.created_at, datetime)

def test_bank_model_name_validation():
    # Testa se o nome do banco respeita as restrições de validação de caracteres e comprimento
    
    # Nome vazio deve falhar
    with pytest.raises(ValidationError):
        BankModel(name="")

    # Nome com mais de 64 caracteres deve falhar
    with pytest.raises(ValidationError):
        BankModel(name="*" * 65)

    # Nome com caracteres válidos deve ser aceito
    bank = BankModel(name="Banco Comum - Á é ç ó")
    assert bank.name == "Banco Comum - Á é ç ó"

    # Nome com vírgula deve falhar
    with pytest.raises(ValidationError):
        BankModel(name="Banco, com vírgula")

def test_bank_model_description_allows_comma():
    # Testa que `description` aceita vírgulas enquanto `name` não permite.
    bank = BankModel(name="Banco Simples", description="Banco de investimento, especializado em tecnologia")
    assert bank.description == "Banco de investimento, especializado em tecnologia"

def test_bank_model_update():
    # Cria uma instância de BankModel e testa a atualização de alguns atributos
    bank = BankModel(name="Banco Original", description="Banco inicial")

    # Define novos valores para atualizar
    updated_data = {
        "name": "Banco Atualizado",
        "description": "Descrição Atualizada, com detalhes",
        "url_image": "https://example.com/logo.png"
    }

    # Realiza a atualização e verifica se uma nova instância foi criada com os valores atualizados
    updated_bank = bank.update(**updated_data)
    assert updated_bank.name == "Banco Atualizado"
    assert updated_bank.description == "Descrição Atualizada, com detalhes"
    assert updated_bank.url_image == "https://example.com/logo.png"
    assert updated_bank.bank_id == bank.bank_id  # `bank_id` não deve mudar
    assert updated_bank.created_at == bank.created_at  # `created_at` não deve mudar

def test_bank_model_created_at_immutable():
    # Testa que o campo `created_at` não é atualizado durante o `update`
    bank = BankModel(name="Banco Teste")
    original_created_at = bank.created_at
    
    # Atualiza o banco, mas sem passar `created_at`
    updated_bank = bank.update(name="Banco Atualizado")
    assert updated_bank.created_at == original_created_at  # `created_at` permanece o mesmo

def test_bank_model_invalid_fields_ignored_in_update():
    # Testa que campos desconhecidos são ignorados durante a atualização
    bank = BankModel(name="Banco Original")
    
    # Tenta atualizar usando um campo inexistente
    with pytest.raises(ValueError, match="O atributo 'unknown_field' não existe na classe BankModel."):
        bank.update(name="Banco Atualizado", unknown_field="Valor Ignorado")
