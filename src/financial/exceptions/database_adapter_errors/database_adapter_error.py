from src.financial.exceptions.base_financial_error import FinancialError
from src.financial.exceptions.code_errors import FinacialErrorGroup, FinacialErrorTag, FinacialErrorType


class DatabaseAdapterError(FinancialError):
    def __init__(self,
                error_tag:FinacialErrorTag=FinacialErrorTag.DATABASE_ADAPTER,
                error_group:FinacialErrorGroup=FinacialErrorGroup.GENERIC,
                error_type: FinacialErrorType = FinacialErrorType.GENERIC,
                error_message: str = "Erro genérico do adaptador de banco de dados",
                **kwargs):
        super().__init__(
            error_tag=error_tag,
            error_group=error_group,
            error_type=error_type,
            error_message=error_message,
            **kwargs
        )
