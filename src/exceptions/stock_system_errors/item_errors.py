from src.exceptions.stock_system_errors.generic_stock_error import StockError
from src.exceptions.error_codes import ErrorCodes


class ItemModelError(StockError):
    """Exceção base para erros relacionados ao modelo de item."""
    pass


class StockValidationError(ItemModelError):
    """Exceção levantada para erros de validação de estoque."""
    def __init__(self):
        error_details = ErrorCodes.ITEM_STOCK_VALIDATION.to_dict()
        super().__init__(error_details['code'], error_details['message'])


class NotEnoughStockError(ItemModelError):
    def __init__(self):
        error_details = ErrorCodes.ITEM_NOT_ENOUGH_STOCK.to_dict()
        super().__init__(error_details['code'], error_details['message'])
