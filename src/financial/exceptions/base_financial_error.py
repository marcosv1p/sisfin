from src.financial.exceptions.code_errors import FinacialErrorGroup, FinacialErrorTag, FinacialErrorType

class FinancialError(Exception):
    def __init__(self,
                error_tag: FinacialErrorTag = FinacialErrorTag.GENERIC,
                error_group: FinacialErrorGroup = FinacialErrorGroup.GENERIC,
                error_type: FinacialErrorType = FinacialErrorType.GENERIC,
                error_message: str = "Erro genérico",
                **kwargs):
        self.error_tag = error_tag
        self.error_group = error_group
        self.error_type = error_type
        self.error_message = error_message
        self.extra_info = kwargs
        tag_str = f"TAG : {self.error_tag}"
        group_str = f"GROUP : {self.error_group}"
        type_str = f"TYPE : {self.error_type}"
        super().__init__(f"[{tag_str} || {group_str} || {type_str}] {self.error_message}")

