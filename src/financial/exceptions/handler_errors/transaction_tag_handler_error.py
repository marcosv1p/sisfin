from src.financial.exceptions.handler_errors.handler_error import HandlerError
from src.financial.exceptions.code_errors import FinacialErrorGroup, FinacialErrorTag, FinacialErrorType


class TransactionTagHandlerError(HandlerError):
    def __init__(self,
                error_tag:FinacialErrorTag=FinacialErrorTag.HANDLER,
                error_group:FinacialErrorGroup=FinacialErrorGroup.ACCOUNT,
                error_type: FinacialErrorType = FinacialErrorType.INVALID_INPUT,
                error_message: str = "Error generico em 'TransactionTagHandler'",
                **kwargs):
        super().__init__(
            error_tag=error_tag,
            error_group=error_group,
            error_type=error_type,
            error_message=error_message,
            **kwargs
        )


class UnexpectedArgumentTypeError(TransactionTagHandlerError):
    def __init__(self,
                error_tag:FinacialErrorTag=FinacialErrorTag.HANDLER,
                error_group:FinacialErrorGroup=FinacialErrorGroup.ACCOUNT,
                error_type: FinacialErrorType = FinacialErrorType.INVALID_INPUT,
                error_message: str = "Tipo de argumento inesperado",
                **kwargs):
        super().__init__(
            error_tag=error_tag,
            error_group=error_group,
            error_type=error_type,
            error_message=error_message,
            **kwargs
        )


class UnexpectedDatabaseTypeError(UnexpectedArgumentTypeError):
    def __init__(self,
                error_tag:FinacialErrorTag=FinacialErrorTag.HANDLER,
                error_group:FinacialErrorGroup=FinacialErrorGroup.ACCOUNT,
                error_type: FinacialErrorType = FinacialErrorType.INVALID_INPUT,
                error_message: str = "Tipo inesperado do argumento 'databese'",
                **kwargs):
        super().__init__(
            error_tag=error_tag,
            error_group=error_group,
            error_type=error_type,
            error_message=error_message,
            **kwargs
        )