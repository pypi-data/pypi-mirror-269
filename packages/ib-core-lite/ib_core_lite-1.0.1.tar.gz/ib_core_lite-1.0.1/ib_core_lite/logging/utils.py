import requests

from ib_core_lite.settings import LOCALHOST
from ib_core_lite.utils import generate_url, check_status_code


def create_log(data: dict, user_id: str) -> tuple[dict, int]:
    response = requests.post(
        generate_url(False, LOCALHOST, 8010, False, "api", "log", "create", container_name="logging-module"),
        headers={"X-UserID": user_id}, json=data)
    if check_status_code(response.status_code):
        return response.json(), response.status_code
    else:
        return dict(detail=response.text), response.status_code
