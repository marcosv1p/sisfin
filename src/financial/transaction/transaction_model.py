import re

from decimal import Decimal
from uuid import UUID, uuid4
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, constr, condecimal

from src.financial.account import AccountModel
from src.financial.transaction import TransactionsTypes


class TransactionModel(BaseModel):
    """
    Representa uma transação financeira entre contas, incluindo data, descrição, valor, e tipos de transação.
    
    ### Atributos:
    - **date** (`datetime`): Data e hora da transação, inicializada com o momento atual.
    - **description** (`str`, opcional): Descrição adicional sobre a transação, com até 255 caracteres. Aceita letras, números, espaços e caracteres especiais (e.g., "- . : ç Ç á Á").
    - **value** (`Decimal`): Valor monetário da transação, com precisão de duas casas decimais. Iniciado com o valor `0.00`.
    - **origin** (`AccountModel`, opcional): Conta de origem da transação, obrigatória apenas para transferências.
    - **transaction_type** (`TransactionsTypes`): Tipo da transação, que pode ser depósito, saque ou transferência.
    - **destination** (`AccountModel`): Conta de destino da transação.
    - **transaction_id** (`UUID`): Identificador único da transação, gerado automaticamente.
    - **created_at** (`datetime`): Data e hora de criação da transação, inicializada automaticamente ao instanciar o modelo.
    - **status** (`bool`): Estado da transação, indicando se ela foi executada (`True`) ou não (`False`).
    """
    date: datetime = Field(default_factory=datetime.now)
    description: constr(max_length=255, pattern=re.compile(r"^[\w\s\-\.,:çÇáÁéÉíÍóÓúÚãÃõÕ]+$", re.UNICODE)) = Field(default=None)
    value: condecimal(decimal_places=2) = Field(default=Decimal("0.00"))
    origin: Optional[AccountModel] = Field(default=None)
    transaction_type: TransactionsTypes
    destination: AccountModel
    
    transaction_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    status: bool = Field(default=False)
    
    def update(self, **kwargs: Any) -> "TransactionModel":
        """
        Retorna uma nova instância de `TransactionModel` com os atributos atualizados.
        
        ### Parâmetros:
        - **kwargs** (`dict`): Dicionário de pares chave-valor representando os atributos e novos valores para atualização.
        
        ### Exemplo de Uso:
        ```python
        transaction = TransactionModel(value=Decimal("100.00"), transaction_type=TransactionsTypes.DEPOSIT)
        updated_transaction = transaction.update(value=Decimal("200.00"))
        ```
        
        ### Notas:
        - A atualização não altera a instância original; em vez disso, retorna uma nova instância com os valores modificados.
        - Somente os atributos válidos serão atualizados; valores desconhecidos serão ignorados.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"O atributo '{key}' não existe na classe TransactionModel.")
            return self
    
    def execute(self) -> None:
        """
        Executa a transação, aplicando a lógica de depósito, saque ou transferência, conforme o tipo de transação.
        
        ### Comportamento:
        - **Depósito**: Adiciona o valor ao saldo da conta de destino.
        - **Saque**: Deduz o valor do saldo da conta de destino.
        - **Transferência**: Deduz o valor do saldo da conta de origem e o adiciona ao saldo da conta de destino.
        
        ### Exceções:
        - Lança `ValueError` se:
            - A transação já tiver sido executada (`status` é `True`).
            - A conta de origem estiver ausente para uma transferência.
            - O tipo de transação for inválido.
        
        ### Exemplo de Uso:
        ```python
        transaction = TransactionModel(value=Decimal("50.00"), transaction_type=TransactionsTypes.DEPOSIT, destination=account)
        transaction.execute()
        ```
        
        ### Notas:
        - Atualiza o atributo `status` para `True` após a execução bem-sucedida.
        - Após executada, uma transação não pode ser reexecutada.
        """
        if not self.status:
            match self.transaction_type:
                case TransactionsTypes.DEPOSIT:
                    self.destination.update(balance=self.destination.balance + self.value)
                case TransactionsTypes.WITHDRAW:
                    self.destination.update(balance=self.destination.balance - self.value)
                case TransactionsTypes.TRANSFER:
                    if not self.origin:
                        raise ValueError("Origin account is required for transfer")
                    self.origin.update(balance=(self.origin.balance - self.value))
                    self.destination.update(balance=self.destination.balance + self.value)
                case _:
                    raise ValueError("Invalid transaction type")
            self.status = True
        else:
            raise ValueError("Invalid transaction type")
    
    def undo_execute(self)  -> None:
        """
        Reverte a transação, desfazendo o impacto financeiro dela na conta(s) envolvida(s).
        
        ### Comportamento:
        - **Depósito**: Deduz o valor do saldo da conta de destino.
        - **Saque**: Adiciona o valor ao saldo da conta de destino.
        - **Transferência**: Reverte o valor da conta de origem e destino.
        
        ### Exceções:
        - Lança `ValueError` se:
            - A transação ainda não tiver sido executada (`status` é `False`).
            - A conta de origem estiver ausente para uma transferência.
            - O tipo de transação for inválido.
        
        ### Exemplo de Uso:
        ```python
        transaction = TransactionModel(value=Decimal("50.00"), transaction_type=TransactionsTypes.WITHDRAW, destination=account)
        transaction.execute()
        transaction.undo_execute()
        ```
        
        ### Notas:
        - Atualiza o atributo `status` para `False` após a reversão bem-sucedida.
        - Após desfeita, uma transação precisa ser executada novamente para ter efeito.
        """
        if self.status:
            match self.transaction_type:
                case TransactionsTypes.DEPOSIT:
                    self.destination.update(balance=self.destination.balance - self.value)
                case TransactionsTypes.WITHDRAW:
                    self.destination.update(balance=self.destination.balance + self.value)
                case TransactionsTypes.TRANSFER:
                    if not self.origin:
                        raise ValueError("Origin account is required for transfer")
                    self.origin.update(balance=(self.origin.balance + self.value))
                    self.destination.update(balance=self.destination.balance - self.value)
                case _:
                    raise ValueError("Invalid transaction type")
            self.status = False
        else:
            raise ValueError("Transaction has not been executed")


