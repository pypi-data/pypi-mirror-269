from abc import ABC, abstractmethod
from typing import Any, List
from uuid import UUID


class Repository(ABC):

    @classmethod
    @abstractmethod
    def get_all(cls) -> List[Any]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_total_count(cls) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_by_id(cls, id: UUID) -> Any:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create(cls, item: Any) -> Any:
        raise NotImplementedError

    @classmethod
    def update(cls, item: Any) -> Any:
        raise NotImplementedError

    @classmethod
    def delete(cls, item: Any) -> None:
        raise NotImplementedError

    @classmethod
    def delete_by_id(cls, id: UUID) -> None:
        raise NotImplementedError
