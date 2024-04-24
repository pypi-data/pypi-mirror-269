from typing import List, TypeVar, Generic
from abc import ABC, abstractmethod
from uuid import UUID
T = TypeVar('T')
class Entity(ABC, Generic[T]):
    """
    The interface for any entity
    """
    def __init__(self,id: UUID = None, name: str = "", description: str = "", parent: object = None) -> None:
        super().__init__()
        self.id = id
        self.parent= parent
        self.name = name
        self.description = description
    @abstractmethod
    def addEntity(self, entity: T) -> bool:
        def add() -> bool:
            return True
        result = add()
        return result
    @abstractmethod
    def removeEntity(self, entity: T) -> bool:
        def remove() -> bool:
            return True
        result = remove()
        return result
    @abstractmethod
    def modifyEntity(self, entity: T) -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    @abstractmethod
    def findEntityByName(self, name: str) -> List[T]:
        def find() -> List[T]:
            return []
        result = find()
        return result
    @abstractmethod
    def findEntityByID(self, name: str) -> List[T]:
        def find() -> List[T]:
            return []
        result = find()
        return result