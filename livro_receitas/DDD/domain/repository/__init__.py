from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Protocol

T = TypeVar('T')

class Repository(ABC, Generic[T]):
	@abstractmethod
	def add(self, entity: T) -> T: ...

	@abstractmethod
	def get(self, entity_id: str) -> Optional[T]: ...

	@abstractmethod
	def list(self) -> List[T]: ...

	@abstractmethod
	def remove(self, entity_id: str) -> None: ...

	@abstractmethod
	def update(self, entity: T) -> T: ...

