import os
from pathlib import Path

from centric_tools import CustomLogger
from centric_tools.interfaces.dag_storage import IDAGStorage


class LocalDAGStorage(IDAGStorage):
    """Handles DAG storage locally in the airflow/dags directory."""

    def __init__(self):
        self.base_dir = Path().absolute()
        self._mount_path = os.environ.get("DAG_MOUNT_PATH")

    def write(self, filename: str, content: str):
        file_path = self.base_dir / f"{self._mount_path}/{filename}"
        with open(file_path, "w") as file:
            file.write(content)

    def delete(self, filename: str) -> bool:
        file_path = self.base_dir / f"{self._mount_path}/{filename}"
        delete_success = False
        if os.path.exists(file_path):
            os.remove(file_path)
            delete_success = True
            CustomLogger.info(f"DAG file {filename} deleted")
        return delete_success


class MountedDAGStorage(IDAGStorage):
    """Handles DAG storage in a mounted directory (e.g., Kubernetes)."""

    def __init__(self):
        self._mount_path = os.environ.get("DAG_MOUNT_PATH")

    def write(self, filename: str, content: str):
        file_path = f"{self._mount_path}/{filename}"
        with open(file_path, "w") as file:
            file.write(content)

    def delete(self, filename: str) -> bool:
        file_path = f"{self._mount_path}/{filename}"
        delete_success = False
        if os.path.exists(file_path):
            os.remove(file_path)
            delete_success = True
            CustomLogger.info(f"DAG file {filename} deleted")
        return delete_success
