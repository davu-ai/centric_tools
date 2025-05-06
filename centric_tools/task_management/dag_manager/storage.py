import os
from pathlib import Path

from centric_tools import CustomLogger
from centric_tools.interfaces.dag_storage import IDAGStorage
from google.cloud import storage
from google.auth import load_credentials_from_dict


class LocalDAGStorage(IDAGStorage):
    """Handles DAG storage locally in the airflow/dags directory."""

    def __init__(self, mount_path: str, **kwargs):
        self.base_dir = Path().absolute()
        self._mount_path = mount_path

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

    def __init__(self, mount_path: str, **kwargs):
        self._mount_path = mount_path

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


class GCPDAGStorage(IDAGStorage):
    def __init__(self, mount_path: str, **kwargs):
        """
        mount_path: this the GCS bucket name e.g "transaction-data"
        kwargs: contains project arg which is the GCP project ID

        """
        self.credentials, _ = load_credentials_from_dict(kwargs.get("credentials"))
        project = kwargs.get("project")

        # This is to enable testing locally without modifying the package
        if kwargs.get("local_test"):
            self._client = storage.Client(project=project)
        else:
            self._client = storage.Client(
                credentials=self.credentials, project=kwargs.get("project")
            )
        self._bucket_name = kwargs.get("bucket_name")
        self._prefix = mount_path

    def _get_blob(self, filename: str) -> storage.Blob:
        full_path = f"{self._prefix}/{filename}" if self._prefix else filename
        bucket = self._client.bucket(self._bucket_name)
        return bucket.blob(full_path)

    def write(self, filename: str, content: str):
        """Write content to a file in the GCS bucket"""
        blob = self._get_blob(filename)
        blob.upload_from_string(content)
        CustomLogger.info(
            f"Uploaded {filename} to gs://{self._bucket_name}/{blob.name}"
        )

    def delete(self, filename: str) -> bool:
        """Delete the file from the GCS bucket"""
        blob = self._get_blob(filename)
        if blob.exists():
            blob.delete()
            CustomLogger.info(f"Deleted gs://{self._bucket_name}/{blob.name}")
            return True
        else:
            CustomLogger.info(
                f"File gs://{self._bucket_name}/{blob.name} does not exist"
            )
            return False


class AWSDAGStorage(IDAGStorage):
    def __init__(self, mount_path: str):
        self._mount_path = mount_path

    def write(self, filename: str, content: str):
        pass

    def delete(self, filename: str) -> bool:
        pass
