from abc import ABC, abstractmethod


class IDagClient(ABC):
    """Interface for Dag client interactions. E.g Airflow, Dagster"""

    @abstractmethod
    def delete_dag(self, dag_id: str) -> bool:
        pass