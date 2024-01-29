from typing import Literal

from tenacity import retry
from tenacity import stop_after_attempt

from backend.src.session import session
from backend.src.settings import settings


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
