from tenacity import retry
from tenacity import stop_after_attempt
import logging

from backend.src.session import session
from backend.src.settings import settings
from utils.main_process import main_process


@retry(stop=stop_after_attempt(10000))
def get_jobs_data(_id: int, _format: str) -> tuple[bytes]:
    """
    Get tuple with 2 archives: images and annotations.
    """
    image_archive_response = session.get(
        url=f"{settings.API_URL}"
            f"/jobs/{_id}"
            f"/data",
        params = {
            "type": "chunk",
            "number": 0,
        },
    )
    
    if image_archive_response.status_code != 200:
        return image_archive_response.status_code

    annotations_archive_response = session.get(
        f"{settings.API_URL}/jobs/{_id}/annotations?action=download&format={_format}",
    )

    image_archive = image_archive_response.content
    annotations_archive = annotations_archive_response.content
    
    if not image_archive or not annotations_archive:
        raise Exception
    
    return image_archive, annotations_archive


@retry(stop=stop_after_attempt(10000))
def get_jobs_list(task_id: int) -> list[int]:
    """
    Get list of jobs from task.
    """
    logging.info(f"Trying to get jobs list from task #{task_id}.")
    jobs = []
    try:
        response = session.get(
            f"{settings.API_URL}/jobs?task_id={task_id}&page_size={1e10}"
        ).json()
        for job in response["results"]:
            jobs.append(int(job["id"]))
        logging.info(f"Seccessfuly getting the jobs list from task #{task_id}.")
    except Exception as e:
        logging.ERROR(f"{repr(e)}: getting jobs id from task #{task_id}.")
    print(jobs)
    return jobs
