from typing import Optional, Any, Protocol


class ProtocolRepository(Protocol):
    def __init__(self, *args, **kargs) -> None:
        ...
    
    def select(self, *args, **kargs) -> list:
        ...
    
    def select_from_id(self, *args, **kargs) -> Optional[Any]:
        ...
    
    def insert(self, *args, **kargs) -> None:
        ...
    
    def update(self, *args, **kargs) -> Optional[Any]:
        ...
    
    def delete(self, *args, **kargs) -> None:
        ...
