from src.financial.exceptions.database_adapter_errors.database_adapter_error import DatabaseAdapterError
from src.financial.exceptions.code_errors import FinacialErrorGroup, FinacialErrorTag, FinacialErrorType


class AccountTagDBAdapterError(DatabaseAdapterError):
    def __init__(self,
                error_tag:FinacialErrorTag=FinacialErrorTag.DATABASE_ADAPTER,
                error_group:FinacialErrorGroup=FinacialErrorGroup.ACCOUNT_TAG,
                error_type: FinacialErrorType = FinacialErrorType.GENERIC,
                error_message: str = "Erro genérico de tag da conta",
                **kwargs):
        super().__init__(
            error_tag=error_tag,
            error_group=error_group,
            error_type=error_type,
            error_message=error_message,
            **kwargs
        )


class AccountTagNotFoundError(AccountTagDBAdapterError):
    def __init__(self,
                error_tag:FinacialErrorTag=FinacialErrorTag.DATABASE_ADAPTER,
                error_group:FinacialErrorGroup=FinacialErrorGroup.ACCOUNT_TAG,
                error_type: FinacialErrorType = FinacialErrorType.NOT_FOUND,
                error_message: str = "Tag da conta não encontrado no banco de dados",
                **kwargs):
        super().__init__(
            error_tag=error_tag,
            error_group=error_group,
            error_type=error_type,
            error_message=error_message,
            **kwargs
        )


class AccountTagAlreadyExistsError(AccountTagDBAdapterError):
    def __init__(self,
                error_tag:FinacialErrorTag=FinacialErrorTag.DATABASE_ADAPTER,
                error_group:FinacialErrorGroup=FinacialErrorGroup.ACCOUNT_TAG,
                error_type: FinacialErrorType = FinacialErrorType.ALREADY_EXISTS,
                error_message: str = "Tag da conta já existe no banco de dados",
                **kwargs):
        super().__init__(
            error_tag=error_tag,
            error_group=error_group,
            error_type=error_type,
            error_message=error_message,
            **kwargs
        )


class UnexpectedArgumentTypeError(AccountTagDBAdapterError):
    def __init__(self,
                error_tag:FinacialErrorTag=FinacialErrorTag.DATABASE_ADAPTER,
                error_group:FinacialErrorGroup=FinacialErrorGroup.ACCOUNT_TAG,
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
