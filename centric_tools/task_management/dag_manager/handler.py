import time

from centric_tools.interfaces.dag_client import IDagClient
from centric_tools.interfaces.dag_storage import IDAGStorage


class DagWriter:
    """Handles writing DAG files using the appropriate storage backend."""

    def __init__(self, storage: IDAGStorage):
        self.storage = storage

    def write_to_dag(self, file_content: str, filename: str):
        self.storage.write(filename, file_content)

    def delete_dag(self, filename: str, dag_id: str, delay: int = 5, client: IDagClient = None):
        if delay:
            time.sleep(delay)
        self.storage.delete(filename)
        if client:
            client.delete_dag(dag_id)
