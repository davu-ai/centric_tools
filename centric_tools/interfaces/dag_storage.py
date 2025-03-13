from abc import ABC, abstractmethod


class IDAGStorage(ABC):
    """Abstract base class for different DAG storage backends."""

    @abstractmethod
    def write(self, filename: str, content: str):
        pass

    @abstractmethod
    def delete(self, filename: str) -> bool:
        pass