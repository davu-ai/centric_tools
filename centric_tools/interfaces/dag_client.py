from abc import ABC, abstractmethod
from typing import Optional


class IDagClient(ABC):
    """Interface for Dag client interactions. E.g Airflow, Dagster"""

    @abstractmethod
    def delete_dag(self, dag_id: str) -> bool:
        pass

    @abstractmethod
    def get_health(self):
        pass

    @abstractmethod
    def trigger_dag_run(self, dag_id: str, conf: Optional[dict] = None) -> bool:
        pass
