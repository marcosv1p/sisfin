from uuid import UUID
from typing import List, Protocol
from abc import ABC, abstractmethod

from infra.repository.protocol import ProtocolRepository


class DataInterface(Protocol):
    id: UUID
    
    def get_current_dict_data(self) -> dict:
        raise NotImplementedError()


class DatabaseAdapterInterface(ABC):
    _db = ProtocolRepository
    
    @classmethod
    @abstractmethod
    def insert(cls, data: DataInterface) -> None:
        raise NotImplementedError()
    
    @classmethod
    @abstractmethod
    def update(cls, id: UUID, data: DataInterface) -> DataInterface:
        raise NotImplementedError()
    
    @classmethod
    @abstractmethod
    def delete(cls, id: UUID) -> None:
        raise NotImplementedError()
    
    @classmethod
    @abstractmethod
    def get(cls, id: UUID) -> DataInterface:
        raise NotImplementedError()
    
    @classmethod
    @abstractmethod
    def get_all(cls) -> List[DataInterface]:
        raise NotImplementedError()
