import re
from datetime import datetime
from pydantic import BaseModel, PrivateAttr, Field, AnyUrl, constr
from uuid import UUID, uuid4
from src.exceptions import StockValidationError, NotEnoughStock
from src.stock_system.validations.item_validators import validate_non_negative, validate_stock_value


class ItemModel(BaseModel):
    """
    Modelo de item que representa um produto no sistema.

    Atributos:
        name (str): Nome do item. Deve ter entre 1 e 64 caracteres e pode conter letras, números, traços e sublinhados.
        description (str): Descrição do item. Máximo de 255 caracteres e pode conter letras, números, traços e sublinhados.
        code (str): Código identificador do item. Máximo de 255 caracteres e pode conter letras, números, traços e sublinhados.
        url (AnyUrl): URL do item. Deve ser uma URL válida.
        date (datetime): Data de criação do item. Definido automaticamente como a data e hora atual no momento da criação.

    Atributos Privados:
        __stock (int): Quantidade de estoque do item. Inicialmente definido como 0.
        __item_id (UUID): Identificador único do item. Gerado automaticamente no momento da criação.
        __created_at (datetime): Data de criação do item. Gerado automaticamente no momento da criação.
    """

    name: constr(min_length=1, max_length=64, pattern=re.compile(r"^[a-zA-Z0-9_-]+$")) = Field(default_factory=lambda: uuid4().hex)
    description: constr(max_length=255, pattern=re.compile(r"^[a-zA-Z0-9_-]*$")) = Field(default=None)
    code: constr(max_length=255, pattern=re.compile(r"^[a-zA-Z0-9_-]*$")) = Field(default=None)
    url: AnyUrl = Field(default=None)
    date: datetime = Field(default_factory=datetime.now)

    __stock: int = PrivateAttr(default=0)
    __item_id: UUID = PrivateAttr(default_factory=uuid4)
    __created_at: datetime = PrivateAttr(default_factory=datetime.now)

    @property
    def stock(self) -> int:
        """
        Retorna a quantidade atual de estoque do item.

        Returns:
            int: A quantidade de estoque disponível para o item.
        """
        return self.__stock

    @property
    def item_id(self) -> str:
        """
        Retorna o ID único do item como uma string hexadecimal.

        Returns:
            str: O ID único do item, representado em formato hexadecimal.
        """
        return self.__item_id.hex

    @property
    def created_at(self) -> datetime:
        """
        Retorna a data de criação do item.

        Returns:
            datetime: A data e hora em que o item foi criado.
        """
        return self.__created_at

    def add_stock(self, value: int) -> None:
        """
        Adiciona uma quantidade ao estoque do item após validação.

        Parâmetros:
            value (int): A quantidade a ser adicionada ao estoque. Deve ser um inteiro não negativo.

        Levanta:
            StockValidationError: Se o valor fornecido for negativo.
        """
        validate_non_negative(value)
        temp_stock = self.__stock + value
        validate_stock_value(stock_value=temp_stock)
        self.__stock = temp_stock
        

    def remove_stock(self, value: int) -> None:
        """
        Remove uma quantidade do estoque do item após validação.

        Parâmetros:
            value (int): A quantidade a ser removida do estoque. Deve ser um inteiro não negativo.

        Levanta:
            StockValidationError: Se o valor fornecido for negativo ou se o estoque atual for insuficiente.
        """
        validate_non_negative(value)
        temp_stock = self.__stock - value
        validate_stock_value(stock_value=temp_stock)
        self.__stock = temp_stock

    def __str__(self) -> str:
        """
        Retorna uma representação em string do modelo de item.

        Returns:
            str: Uma string formatada contendo informações principais do item, incluindo nome, estoque, item_id e data de criação.
        """
        return f"ItemModel(nome={self.name}, estoque={self.stock}, item_id={self.item_id}, criado_em={self.created_at})"

    def to_dict(self) -> dict:
        """
        Retorna uma representação do modelo de item como um dicionário.

        Returns:
            dict: Um dicionário contendo todos os atributos públicos do item.
        """
        return {
            "nome": self.name,
            "descricao": self.description,
            "codigo": self.code,
            "url": str(self.url),
            "data": self.date.isoformat(),
            "estoque": self.stock,
            "item_id": self.item_id,
            "criado_em": self.created_at.isoformat()
        }
