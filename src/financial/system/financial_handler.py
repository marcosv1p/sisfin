from uuid import UUID
from typing import List, Optional

from src.financial.bank import BankModel
from src.financial.account import AccountModel
from src.financial.transaction import TransactionModel
from src.financial.database_handler import DatabaseHandler
from src.financial.exceptions.financial_handler_error import (
    BankNotFoundError,
    BankAccountNotFoundError,
    TransactionNotFoundError,
    BankAlreadyExistsError,
    BankAccountAlreadyExistsError,
    TransactionAlreadyExistsError,
)


class FinancialHandler:
    def __init__(self) -> None:
        self.load_all_data()
    
    def load_all_data(self) -> None:
        """
        Carrega todos os dados de bancos, contas e transações.
        
        ### Comportamento:
        - Invoca métodos privados para carregar os dados necessários.
        """
        self._load_banks()
        self._load_accounts()
        self._load_transactions()
    
    def _load_banks(self) -> List[BankModel]:
        """
        Carrega todos os bancos do banco de dados.
        
        ### Retorno:
        - (`List[BankModel]`): Lista de modelos de bancos.
        
        ### Comportamento:
        - Os bancos são carregados apenas uma vez e armazenados em cache.
        """
        if not hasattr(self, '_banks'):
            self._banks = DatabaseHandler.db_bank.get_all()
        return self._banks
    
    def _load_accounts(self) -> List[AccountModel]:
        """
        Carrega todas as contas do banco de dados.
        
        ### Retorno:
        - (`List[AccountModel]`): Lista de modelos de contas.
        
        ### Comportamento:
        - Os dados são carregados após os bancos serem carregados.
        """
        if not hasattr(self, '_accounts'):
            self._load_banks()
            self._accounts = DatabaseHandler.db_account.get_all()
        return self._accounts
    
    def _load_transactions(self) -> List[TransactionModel]:
        """
        Carrega todas as transações do banco de dados.
        
        ### Retorno:
        - (`List[TransactionModel]`): Lista de modelos de transações.
        
        ### Comportamento:
        - Os dados são carregados após as contas serem carregadas.
        """
        if not hasattr(self, '_transactions'):
            self._load_accounts()
            self._transactions = DatabaseHandler.db_transaction.get_all()
        return self._transactions
    
    def add_bank(self, bank: BankModel) -> None:
        """
        Adiciona um novo banco ao banco de dados.
        
        ### Parâmetros:
        - **bank** (`BankModel`): Instância de `BankModel` representando o banco a ser adicionado.
        
        ### Comportamento:
        - Verifica se o banco já existe. Se existir, lança `BankAlreadyExistsError`.
        - Insere o novo banco e atualiza a lista de bancos.
        """
        assert isinstance(bank, BankModel)
        existing_bank = DatabaseHandler.db_bank.get(bank_id=bank.bank_id)
        if existing_bank:
            raise BankAlreadyExistsError(existing_bank.bank_id)
        DatabaseHandler.db_bank.insert(bank=bank)
        self._load_banks()
    
    def add_account(self, account: AccountModel) -> None:
        """
        Adiciona uma nova conta ao banco de dados.
        
        ### Parâmetros:
        - **account** (`AccountModel`): Instância de `AccountModel` representando a conta a ser adicionada.
        
        ### Comportamento:
        - Verifica se a conta já existe. Se existir, lança `BankAccountAlreadyExistsError`.
        - Insere a nova conta e atualiza a lista de contas.
        """
        assert isinstance(account, AccountModel)
        existing_account = DatabaseHandler.db_account.get(account_id=account.account_id)
        if existing_account:
            raise BankAccountAlreadyExistsError(existing_account.account_id)
        DatabaseHandler.db_account.insert(account=account)
        self._load_accounts()
    
    def add_transaction(self, transaction: TransactionModel) -> None:
        """
        Adiciona uma nova transação ao banco de dados.
        
        ### Parâmetros:
        - **transaction** (`TransactionModel`): Instância de `TransactionModel` representando a transação a ser adicionada.
        
        ### Comportamento:
        - Verifica se a transação já existe. Se existir, lança `TransactionAlreadyExistsError`.
        - Insere a nova transação e atualiza a lista de transações.
        """
        assert isinstance(transaction, TransactionModel)
        existing_transaction = DatabaseHandler.db_transaction.get(transaction_id=transaction.transaction_id)
        if existing_transaction:
            raise TransactionAlreadyExistsError(existing_transaction.transaction_id)
        DatabaseHandler.db_transaction.insert(transaction=transaction)
        self._load_transactions()
        self._execute_transaction(transaction_id=transaction.transaction_id)
    
    def update_bank(self, bank_id: UUID, bank: BankModel) -> None:
        """
        Atualiza os dados de um banco existente.
        
        ### Parâmetros:
        - **bank_id** (`UUID`): Identificador único do banco a ser atualizado.
        - **bank** (`BankModel`): Instância de `BankModel` com os novos dados do banco.
        
        ### Comportamento:
        - Verifica se o banco existe. Se existir, atualiza os dados e a lista de bancos.
        - Se o banco não for encontrado, lança `BankNotFoundError`.
        """
        existing_bank = DatabaseHandler.db_bank.get(bank_id=bank.bank_id)
        if existing_bank:
            DatabaseHandler.db_bank.update(bank_id=bank_id, bank=bank)
            self._load_banks()
        else:
            raise BankNotFoundError(bank_id=bank.bank_id)
    
    def update_account(self, account_id: UUID, account: AccountModel) -> None:
        """
        Atualiza os dados de uma conta existente.
        
        ### Parâmetros:
        - **account_id** (`UUID`): Identificador único da conta a ser atualizada.
        - **account** (`AccountModel`): Instância de `AccountModel` com os novos dados da conta.
        
        ### Comportamento:
        - Verifica se a conta existe. Se existir, atualiza os dados e a lista de contas.
        - Se a conta não for encontrada, lança `BankAccountNotFoundError`.
        """
        existing_account = DatabaseHandler.db_account.get(account_id=account.account_id)
        if existing_account:
            DatabaseHandler.db_account.update(account_id=account_id, account=account)
            self._load_accounts()
        else:
            raise BankAccountNotFoundError(account_id=account_id)
    
    def update_transaction(self, transaction_id: UUID, transaction: TransactionModel) -> None:
        """
        Atualiza os dados de uma transação existente.
        
        ### Parâmetros:
        - **transaction_id** (`UUID`): Identificador único da transação a ser atualizada.
        - **transaction** (`TransactionModel`): Instância de `TransactionModel` com os novos dados da transação.
        
        ### Comportamento:
        - Verifica se a transação existe. Se existir, atualiza os dados e a lista de transações.
        - Se a transação não for encontrada, lança `TransactionNotFoundError`.
        """
        existing_transaction = DatabaseHandler.db_transaction.get(transaction_id=transaction.transaction_id)
        if existing_transaction:
            DatabaseHandler.db_transaction.update(transaction_id=transaction_id, transaction=transaction)
            self._load_transactions()
        else:
            raise TransactionNotFoundError(transaction_id=transaction_id)
    
    def remove_bank(self, bank_id: UUID) -> None:
        """
        Remove um banco do banco de dados.
        
        ### Parâmetros:
        - **bank_id** (`UUID`): Identificador único do banco a ser removido.
        
        ### Comportamento:
        - Deleta o banco e atualiza a lista de bancos.
        """
        assert isinstance(bank_id, UUID)
        DatabaseHandler.db_bank.delete(bank_id=bank_id)
        self._load_banks()
    
    def remove_account(self, account_id: UUID) -> None:
        """
        Remove uma conta do banco de dados.
        
        ### Parâmetros:
        - **account_id** (`UUID`): Identificador único da conta a ser removida.
        
        ### Comportamento:
        - Deleta a conta e recarrega todos os dados.
        """
        assert isinstance(account_id, UUID)
        DatabaseHandler.db_account.delete(account_id=account_id)
        self.load_all_data()
    
    def remove_transaction(self, transaction_id: UUID) -> None:
        """
        Remove uma transação do banco de dados.
        
        ### Parâmetros:
        - **transaction_id** (`UUID`): Identificador único da transação a ser removida.
        
        ### Comportamento:
        - Deleta a transação e recarrega todos os dados.
        """
        assert isinstance(transaction_id, UUID)
        self._undo_execute_transaction(transaction_id=transaction_id)
        DatabaseHandler.db_transaction.delete(transaction_id=transaction_id)
        self.load_all_data()
    
    def get_bank(self, bank_id: UUID) -> Optional[BankModel]:
        """
        Obtém um banco pelo seu ID.
        
        ### Parâmetros:
        - **bank_id** (`UUID`): Identificador único do banco desejado.
        
        ### Retorno:
        - (`Optional[BankModel]`): Instância de `BankModel` correspondente ao `bank_id`, ou `None` se não encontrado.
        """
        return DatabaseHandler.db_bank.get(bank_id=bank_id)
    
    def get_account(self, account_id: UUID) -> Optional[AccountModel]:
        """
        Obtém uma conta pelo seu ID.
        
        ### Parâmetros:
        - **account_id** (`UUID`): Identificador único da conta desejada.
        
        ### Retorno:
        - (`Optional[AccountModel]`): Instância de `AccountModel` correspondente ao `account_id`, ou `None` se não encontrado.
        """
        return DatabaseHandler.db_account.get(account_id=account_id)
    
    def get_transaction(self, transaction_id: UUID) -> Optional[TransactionModel]:
        """
        Obtém uma transação pelo seu ID.
        
        ### Parâmetros:
        - **transaction_id** (`UUID`): Identificador único da transação desejada.
        
        ### Retorno:
        - (`Optional[TransactionModel]`): Instância de `TransactionModel` correspondente ao `transaction_id`, ou `None` se não encontrado.
        """
        return DatabaseHandler.db_transaction.get(transaction_id=transaction_id)
    
    def get_all_banks(self) -> List[BankModel]:
        """
        Obtém todas as instâncias de `BankModel`.
        
        ### Retorno:
        - (`List[BankModel]`): Lista de todos os bancos.
        """
        return DatabaseHandler.db_bank.get_all()
    
    def get_all_accounts(self) -> List[AccountModel]:
        """
        Obtém todas as instâncias de `AccountModel`.
        
        ### Retorno:
        - (`List[AccountModel]`): Lista de todas as contas.
        """
        return DatabaseHandler.db_account.get_all()
    
    def get_all_transactions(self) -> List[TransactionModel]:
        """
        Obtém todas as instâncias de `TransactionModel`.
        
        ### Retorno:
        - (`List[TransactionModel]`): Lista de todas as transações.
        """
        return DatabaseHandler.db_transaction.get_all()
    
    def _execute_transaction(self, transaction_id: UUID) -> None:
        """
        Executa uma transação pelo seu ID.
        
        ### Parâmetros:
        - **transaction_id** (`UUID`): Identificador único da transação a ser executada.
        
        ### Comportamento:
        - Atualiza as contas de origem e destino após a execução da transação.
        - Lança `TransactionNotFoundError` se a transação não for encontrada.
        """
        assert isinstance(transaction_id, UUID)
        transaction = DatabaseHandler.db_transaction.get(transaction_id=transaction_id)
        if transaction:
            if not transaction.status:
                self._load_accounts()
                # Executa a transação
                transaction.execute()
                DatabaseHandler.db_transaction.update(transaction_id=transaction_id, transaction=transaction)
                self._load_transactions()
                
                # Retorna e registra a conta de destino modificada
                destination = transaction.destination
                DatabaseHandler.db_account.update(account_id=destination.account_id, account=destination)
                
                # Retorna e registra a conta de origim modificada caso existir
                if origin:=transaction.origin:
                    DatabaseHandler.db_account.update(account_id=origin.account_id, account=origin)
                
                # Certifica que o FanacialHandler esteja atualizado
                self._load_accounts()
        else:
            raise TransactionNotFoundError(transaction_id=transaction_id)
    
    def _undo_execute_transaction(self, transaction_id: UUID) -> None:
        """
        Reverte a execução de uma transação pelo seu ID.
        
        ### Parâmetros:
        - **transaction_id** (`UUID`): Identificador único da transação a ser revertida.
        
        ### Comportamento:
        - Atualiza as contas de origem e destino após a reversão da transação.
        - Lança `TransactionNotFoundError` se a transação não for encontrada.
        """
        assert isinstance(transaction_id, UUID)
        transaction = DatabaseHandler.db_transaction.get(transaction_id=transaction_id)
        if transaction:
            if transaction.status:
                # Reverte a transação
                transaction.undo_execute()
                DatabaseHandler.db_transaction.update(transaction_id=transaction_id, transaction=transaction)
                
                # Retorna e registra a conta de destino modificada
                destination = transaction.destination
                DatabaseHandler.db_account.insert(account=destination)
                
                # Retorna e registra a conta de origim modificada caso existir
                if origin:=transaction.origin:
                    DatabaseHandler.db_account.insert(account=origin)
                
                
                # Certifica que o FanacialHandler esteja atualizado
                self._load_accounts()
                self._load_transactions()
        else:
            raise TransactionNotFoundError(transaction_id=transaction_id)




