from uuid import UUID
from typing import List, Optional
from datetime import datetime

from infra import BankRepository
from src.financial.bank import BankModel


class BankDatabaseHandler:
    _db = BankRepository()
    
    @classmethod
    def insert(cls, bank: BankModel) -> None:
        """
        Insere um novo banco no banco de dados. Se o banco já existir, ele é substituído.
        
        ### Parâmetros:
        - **bank** (`BankModel`): Instância de `BankModel` representando o banco a ser inserido
        
        ### Comportamento:
        - Verifica se já existe um banco com o `bank_id` fornecido.
        - Se existir, o banco antigo é removido antes de inserir o novo.
        
        ### Exemplo de Uso:
        ```python
        new_bank = BankModel(name="Novo Banco", description="Banco de exemplo")
        BankDatabaseHandler.insert(new_bank)
        ```
        """
        result = cls._db.select_from_id(bank.bank_id.hex)
        if result:
            cls._db.delete(bank_id=bank.bank_id.hex)
        cls._db.insert(
            bank_id=bank.bank_id.hex,
            name=bank.name,
            description=bank.description,
            created_at=bank.created_at,
            url_image=bank.url_image,
        )
    
    @classmethod
    def update(cls, bank_id: UUID, bank: BankModel) -> None:
        """
        Atualiza os dados de um banco existente no banco de dados.
        
        ### Parâmetros:
        - **bank_id** (`UUID`): Identificador único do banco a ser atualizado.
        - **bank** (`BankModel`): Instância de `BankModel` com os novos dados do banco.
        
        ### Comportamento:
        - Obtém o banco existente pelo `bank_id`.
        - Verifica e aplica as mudanças nos campos que foram atualizados.
        
        ### Exemplo de Uso:
        ```python
        updated_bank = BankModel(name="Banco Atualizado", description="Nova descrição")
        BankDatabaseHandler.update(bank_id=UUID("id_do_banco"), bank=updated_bank)
        ```
        """
        current_bank = cls._db.select_from_id(bank_id=bank_id.hex)
        
        if not current_bank:
            raise ValueError("Banco não encontrado.")
        
        updates = {}
        if bank.bank_id and bank.bank_id != UUID(current_bank.bank_id):
            updates['new_bank_id'] = bank.bank_id.hex
        
        if bank.name and bank.name != current_bank.name:
            updates['new_name'] = bank.name
        
        if bank.description and bank.description != current_bank.description:
            updates['new_description'] = bank.description
        
        if bank.created_at and bank.created_at != current_bank.created_at:
            updates['new_created_at'] = bank.created_at
        
        if bank.url_image and bank.url_image != current_bank.url_image:
            updates['new_url_image'] = bank.url_image
        
        if updates:
            cls._db.update(
                bank_id=bank_id.hex,
                new_bank_id=updates.get("new_bank_id"),
                name=updates.get("new_name"),
                description=updates.get("new_description"),
                created_at=updates.get("new_created_at"),
                url_image=updates.get("new_url_image")
            )
    
    @classmethod
    def delete(cls, bank_id: UUID) -> None:
        """
        Deleta um banco do banco de dados com base no ID fornecido.
        
        ### Parâmetros:
        - **bank_id** (`UUID`): Identificador único do banco a ser deletado.
        
        ### Exemplo de Uso:
        ```python
        BankDatabaseHandler.delete(UUID("id_do_banco"))
        ```
        """
        cls._db.delete(bank_id.hex)
    
    @classmethod
    def get(cls, bank_id: UUID) -> Optional[BankModel]:
        """
        Obtém uma instância de `BankModel` pelo `bank_id` fornecido.
        
        ### Parâmetros:
        - **bank_id** (`UUID`): Identificador único do banco desejado.
        
        ### Retorno:
        - (`Optional[BankModel]`): Instância de `BankModel` correspondente ao `bank_id`, ou `None` se o banco não for encontrado.
        
        ### Exemplo de Uso:
        ```python
        bank = BankDatabaseHandler.get(UUID("id_do_banco"))
        ```
        """
        raw_data = cls._db.select_from_id(bank_id.hex)
        if raw_data:
            data = raw_data.to_dict()
            data.update(
                bank_id=bank_id,
                created_at=datetime.fromisoformat(data.get("created_at"))
                )
            return BankModel(**data)
        return None
    
    @classmethod
    def get_all(cls) -> List[BankModel]:
        """
        Obtém todas as instâncias de `BankModel` presentes no banco de dados.
        
        ### Retorno:
        - (`List[BankModel]`): Lista de todas as instâncias de `BankModel`.
        
        ### Exemplo de Uso:
        ```python
        all_banks = BankDatabaseHandler.get_all()
        ```
        """
        """Obtém todos os bancos."""
        raw_data = cls._db.select()
        if raw_data:
            data = []
            for bank in raw_data:
                d = bank.to_dict()
                d.update(
                    bank_id=UUID(d.get("bank_id")),
                    created_at=datetime.fromisoformat(d.get("created_at"))
                )
                data.append(BankModel(**d))
            return data
        return []
