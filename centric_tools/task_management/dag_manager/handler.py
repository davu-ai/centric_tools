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
        delete_success = self.storage.delete(filename)
        if delete_success and client:
            # NOTE: We only delete the dag reference if the file
            # is deleted successfully because, if the dag reference is deleted and the
            # file still exists in the dag bag the client will have no knowledge of the dag because the reference
            # was deleted and treat the dag as new and rerun it again which wil result in an infinite loop of dag reference deletion and
            # dag rerun
            client.delete_dag(dag_id)
