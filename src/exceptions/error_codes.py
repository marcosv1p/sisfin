from enum import Enum


class ErrorCodes(Enum):
    ITEM_STOCK_VALIDATION = ("S001", "Valor de estoque inválido. Deve ser um inteiro não negativo.")
    ITEM_NOT_ENOUGH_STOCK = ("S002", "Sem estoque suficiente.")
    
    USER_NOT_FOUND = ("U001", "Usuário não encontrado no banco de dados.")
    INVALID_USER_ID = ("U002", "ID de usuário inválido fornecido.")
    
    PASSWORD_TOO_SHORT = ("P001", "A senha deve ter pelo menos 8 caracteres.")
    PASSWORD_MISSING_UPPERCASE = ("P002", "A senha deve conter pelo menos uma letra maiúscula.")
    PASSWORD_MISSING_LOWERCASE = ("P003", "A senha deve conter pelo menos uma letra minúscula.")
    PASSWORD_MISSING_DIGIT = ("P004", "A senha deve conter pelo menos um número.")
    PASSWORD_MISSING_SPECIAL_CHAR = ("P005", "A senha deve conter pelo menos um caractere especial.")
    
    AUTH_INVALID_CREDENTIALS = ("A001", "Credenciais de autenticação inválidas.")
    AUTH_TOKEN_EXPIRED = ("A002", "O token de autenticação expirou.")
    
    DB_CONNECTION_FAILED = ("D001", "Falha ao conectar ao banco de dados.")
    DB_DUPLICATE_ENTRY = ("D002", "Entrada duplicada no banco de dados.")
    
    UNKNOWN_ERROR = ("G001", "Ocorreu um erro desconhecido.")

    @property
    def code(self) -> str:
        """Retorna o código do erro."""
        return self.value[0]

    @property
    def message(self) -> str:
        """Retorna a mensagem do erro."""
        return self.value[1]

    def to_dict(self) -> dict:
        """Retorna um dicionário contendo o código e a mensagem do erro."""
        return {"code": self.code, "message": self.message}
