from typing import Literal

import requests
from tenacity import retry
from tenacity import stop_after_attempt

from backend.src.settings import settings

session = requests.Session()
session.auth = (settings.USERNAME, settings.PASSWORD)


@retry(stop=stop_after_attempt(10))
def get_data(
    _type: Literal["jobs", "tasks"], _id: int, _format: str
) -> tuple[bytes]:
    """
    Get tuple with 2 archives: images and annotations.
    """
    archive = session.get(
        f"{settings.API_URL}/{_type}/{_id}/data?type=chunk&number=0",
    ).content

    annotations = session.get(
        f"{settings.API_URL}/{_type}/{_id}/annotations?action=download&format={_format}",
    ).content

    if not archive or not annotations:
        raise Exception

    return archive, annotations
