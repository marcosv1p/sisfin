from typing import Callable, Any, Optional


class FinancialOnErrorEvent:
    def __init__(self, error: Exception):
        self.error = error


class FinancialOnErrorToCallList:
    _ON_ERROR_TO_CALL_LIST = list()
    
    @classmethod
    def add_function(cls, func: Callable[..., Any]) -> None:
        cls._ON_ERROR_TO_CALL_LIST.append(func)
    
    @classmethod
    def remove_function(cls, func: Callable[..., Any]) -> None:
        cls._ON_ERROR_TO_CALL_LIST.remove(func)
    
    @classmethod
    def to_call_list(cls):
        return cls._ON_ERROR_TO_CALL_LIST


class FinancialOnErrorManager:
    _financial_on_error_to_call_list = FinancialOnErrorToCallList
    
    @classmethod
    def on_error(cls, func: Callable[..., Any]) -> Callable[..., Any]:
        cls._financial_on_error_to_call_list.add_function(func=func)
        return func
    
    @classmethod
    def _trigger_on_error(cls, func: Callable[..., Any]) -> Optional[Callable[..., Any]]:
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as exc:
                if to_call_list:=cls._financial_on_error_to_call_list.to_call_list():
                    for to_call in to_call_list:
                        to_call(FinancialOnErrorEvent(error=exc))
                else:
                    print("{"+f"FinancialOnErrorManager:{exc}"+"}")
                return None
        return wrapper