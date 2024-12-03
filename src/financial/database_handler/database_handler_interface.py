
class DatabaseHandlerInterface:
    _db = None
    
    @classmethod
    def insert(cls) -> None:
        raise NotImplementedError()
    
    @classmethod
    def update(cls) -> None:
        raise NotImplementedError()
    
    @classmethod
    def delete(cls) -> None:
        raise NotImplementedError()
    
    @classmethod
    def get(cls) -> None:
        raise NotImplementedError()
    
    @classmethod
    def get_all(cls) -> None:
        raise NotImplementedError()
