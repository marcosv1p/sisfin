from uuid import UUID
from typing import List
from decimal import Decimal
from datetime import datetime

from infra import TransactionRepository
from src.financial.transaction import TransactionModel
from src.financial.database_handler.account_handler import AccountDatabaseHandler


class TransactionDatabaseHandler:
    _db = TransactionRepository()
    
    @classmethod
    def insert(cls, transaction: TransactionModel) -> None:
        """
        Insere uma nova transação no banco de dados. Se a transação já existir, ela é substituída.
        
        ### Parâmetros:
        - **transaction** (`TransactionModel`): Instância de `TransactionModel` representando a transação a ser inserida.
        
        ### Comportamento:
        - Verifica se já existe uma transação com o `transaction_id` fornecido.
        - Se existir, a transação antiga é removida antes de inserir a nova.
        
        ### Exemplo de Uso:
        ```python
        new_transaction = TransactionModel(description="Pagamento", value=Decimal("500.00"))
        TransactionDatabaseHandler.insert(new_transaction)
        ```
        """
        result = cls._db.select_from_id(transaction.transaction_id.hex)
        if result:
            cls._db.delete(account_id=transaction.account_id.hex)
        
        cls._db.insert(
            transaction_id=transaction.transaction_id.hex,
            date=transaction.date,
            description=transaction.description,
            value=transaction.value,
            transaction_type=transaction.transaction_type.value,
            origin=transaction.origin.account_id.hex if transaction.origin else None,
            destination=transaction.destination.account_id.hex,
            status=transaction.status,
            created_at=transaction.created_at
        )
    
    @classmethod
    def update(cls, transaction_id: UUID, transaction: TransactionModel) -> None:
        """
        Atualiza os dados de uma transação existente no banco de dados, aplicando apenas os campos alterados.
        
        ### Parâmetros:
        - **transaction_id** (`UUID`): Identificador único da transação a ser atualizada.
        - **transaction** (`TransactionModel`): Instância de `TransactionModel` com os novos dados da transação.
        
        ### Comportamento:
        - Obtém a transação existente pelo `transaction_id`.
        - Verifica e aplica as mudanças nos campos que foram atualizados.
        
        ### Exemplo de Uso:
        ```python
        updated_transaction = TransactionModel(description="Transferência Atualizada", value=Decimal("300.00"))
        TransactionDatabaseHandler.update(transaction_id=UUID("id_da_transacao"), transaction=updated_transaction)
        ```
        """
        
        # Obter os dados atuais da transação
        current_transaction = cls._db.select_from_id(transaction_id=transaction_id.hex)
        
        if not current_transaction:
            raise ValueError("Transação não encontrada.")
        
        # Dicionário para campos modificados
        updates = {}
        if transaction.transaction_id and transaction.transaction_id != transaction.transaction_id:
            updates['transaction_id'] = transaction.transaction_id.hex
        
        # Comparar e adicionar campos alterados ao dicionário `updates`
        if transaction.description and transaction.description != current_transaction.description:
            updates['new_description'] = transaction.description
        
        if transaction.value and transaction.value != current_transaction.value:
            updates['new_value'] = transaction.value
        
        if transaction.transaction_type and transaction.transaction_type.value != current_transaction.transaction_type:
            updates['new_transaction_type'] = transaction.transaction_type.value
        
        if transaction.origin and transaction.origin.account_id.hex != (current_transaction.origin if current_transaction.origin else None):
            updates['new_origin'] = transaction.origin.account_id.hex
        elif not transaction.origin:
            updates['new_origin'] = None  # Remove a origem se não estiver definida
        
        if transaction.destination and transaction.destination.account_id.hex != current_transaction.destination:
            updates['new_destination'] = transaction.destination.account_id.hex
        
        if transaction.status is not None and transaction.status != current_transaction.status:
            updates['new_status'] = transaction.status
        
        # Executa o update apenas se houver campos alterados
        if updates:
            cls._db.update(
                transaction_id=transaction_id.hex,
                new_description=updates.get("new_description"),
                new_value=updates.get("new_value"),
                new_transaction_type=updates.get("new_transaction_type"),
                new_origin=updates.get("new_origin"),
                new_destination=updates.get("new_destination"),
                new_status=updates.get("new_status")
            )
    
    @classmethod
    def delete(cls, transaction_id: UUID) -> None:
        """
        Deleta uma transação do banco de dados com base no ID fornecido.
        
        ### Parâmetros:
        - **transaction_id** (`UUID`): Identificador único da transação a ser deletada.
        
        ### Exemplo de Uso:
        ```python
        TransactionDatabaseHandler.delete(UUID("id_da_transacao"))
        ```
        """
        cls._db.delete(transaction_id=transaction_id.hex)
    
    @classmethod
    def get(cls, transaction_id: UUID) -> TransactionModel:
        """
        Obtém uma instância de `TransactionModel` pelo `transaction_id` fornecido.
        
        ### Parâmetros:
        - **transaction_id** (`UUID`): Identificador único da transação desejada.
        
        ### Retorno:
        - (`Optional[TransactionModel]`): Instância de `TransactionModel` correspondente ao `transaction_id`, ou `None` se a transação não for encontrada.
        
        ### Exemplo de Uso:
        ```python
        transaction = TransactionDatabaseHandler.get(UUID("id_da_transacao"))
        ```
        """
        raw_data = cls._db.select_from_id(transaction_id=transaction_id.hex)
        if raw_data:
            data = raw_data.to_dict()
            data.update(
                date=datetime.fromisoformat(data.get("date")),
                value=Decimal(data.get("value")),
                origin=AccountDatabaseHandler.get(UUID(data.get("origin"))) if data.get("origin") else None,
                destination=AccountDatabaseHandler.get(UUID(data.get("destination"))),
                transaction_id=transaction_id,
                created_at=datetime.fromisoformat(data.get("created_at")),
                )
            
            # date: datetime = datetime.now,
            # description: Any = None,
            # value: Any = Decimal("0.00"),
            # origin: AccountModel | None = None,
            # transaction_type: TransactionsTypes,
            # destination: AccountModel,
            # transaction_id: UUID = uuid4,
            # created_at: datetime = datetime.now,
            # status: bool = False
            return TransactionModel(**data)
        return None
    
    @classmethod
    def get_all(cls) -> List[TransactionModel]:
        """
        Obtém todas as instâncias de `TransactionModel` presentes no banco de dados.
        
        ### Retorno:
        - (`List[TransactionModel]`): Lista de todas as instâncias de `TransactionModel`.
        
        ### Exemplo de Uso:
        ```python
        all_transactions = TransactionDatabaseHandler.get_all()
        ```
        """
        raw_data = cls._db.select()
        if raw_data:
            data = []
            for transaction in raw_data:
                data.append(cls.get(transaction_id=UUID(transaction.transaction_id)))
            return data
        return []
