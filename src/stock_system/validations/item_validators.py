from src.exceptions import StockValidationError, NotEnoughStockError


def validate_stock_value(stock_value: int) -> bool:
    """Valida se o valor fornecido é um inteiro não negativo."""
    if not isinstance(stock_value, int):
        raise ValueError("O valor deve ser um inteiro.")
    if stock_value < 0:
        raise NotEnoughStockError()
    return True


def validate_non_negative(value: int) -> bool:
    """Valida se o valor fornecido é um inteiro não negativo."""
    if not isinstance(value, int):
        raise ValueError("O valor deve ser um inteiro.")
    if value < 0:
        raise StockValidationError()
    return True
