from typing import Dict, List, Generic, TypeVar, Optional

from domain.repository import Repository

T = TypeVar('T')

class InMemoryRepository(Repository[T], Generic[T]):
    def __init__(self):
        self._data: Dict[str, T] = {}

    def add(self, entity: T) -> T:
        entity_id = getattr(entity, 'id', None)
        if entity_id is None:
            raise ValueError('Entity must have an id attribute')
        self._data[entity_id] = entity
        return entity

    def get(self, entity_id: str) -> Optional[T]:
        return self._data.get(entity_id)

    def list(self) -> List[T]:
        return list(self._data.values())

    def remove(self, entity_id: str) -> None:
        if entity_id in self._data:
            del self._data[entity_id]

    def update(self, entity: T) -> T:
        entity_id = getattr(entity, 'id', None)
        if entity_id is None or entity_id not in self._data:
            raise ValueError('Entity must exist to be updated')
        self._data[entity_id] = entity
        return entity
