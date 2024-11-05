class GenericUserError(Exception):
    """Classe genérica para erros relacionados a usuários."""
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
