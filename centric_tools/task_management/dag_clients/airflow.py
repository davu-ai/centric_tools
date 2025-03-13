import base64
import os
import requests

from centric_tools import CustomLogger
from centric_tools.interfaces.dag_client import IDagClient


class AirflowClient(IDagClient):

    def __init__(self):
        self._auth_type = os.environ.get("AIRFLOW_AUTH_TYPE") or "login/password"  # Other option: "auth_token"
        self._base_url = os.environ.get("AIRFLOW_BASE_URL")
        self._airflow_api_key = os.environ.get("AIRFLOW_API_KEY")
        self._airflow_username = os.environ.get("AIRFLOW_USERNAME")
        self._airflow_password = os.environ.get("AIRFLOW_PASSWORD")

    def get_authorization(self) -> str:
        if self._auth_type == "auth_token":
            return f"Bearer {self._airflow_api_key}"

        elif self._auth_type == "login/password":
            input_string = f"{self._airflow_username}:{self._airflow_password}"
            encoded_bytes = base64.b64encode(input_string.encode("utf-8"))
            return f"Basic {encoded_bytes.decode('utf-8')}"
        return ""

    def _initiate_request(self, endpoint: str, payload=None, method="GET"):

        url = f"{self._base_url}{endpoint}"
        headers = {
            "Accept": "application/json",
            "Authorization": self.get_authorization(),
        }
        try:
            response = requests.request(method, url, headers=headers, json=payload)
            return response
        except requests.RequestException as e:
            CustomLogger.info(f"Airflow request failed: {e}")
            return None

    def delete_dag(self, dag_id: str) -> bool:
        endpoint = f"/dags/{dag_id}"
        response = self._initiate_request(endpoint, method="DELETE")

        if response is None:
            CustomLogger.info(f"Failed to delete DAG {dag_id}")
            return False
        if response.status_code != 204:
            CustomLogger.info(f"Failed to delete DAG {dag_id}", context={"reason": str(response.json())})

        else:
            CustomLogger.info(f"DAG {dag_id} deleted with status {response.status_code}")
        return response.status_code == 204

    def get_health(self) -> dict:
        endpoint = "/health"
        try:
            response = self._initiate_request(endpoint)
            status_code = response.status_code
            response_data = response.json()
        except Exception as e:
            status_code = 500
            response_data = {"error": str(e)}
        return {"response_data": response_data, "status_code": status_code}
