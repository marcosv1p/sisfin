
class StockError(Exception):
    """Exceção base para erros relacionados ao estoque."""
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
