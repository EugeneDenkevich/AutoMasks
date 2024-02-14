from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import retry_if_exception_type
import logging

from backend.src.session import session
from backend.src.settings import settings
from backend.src.exceprions import RetryExceprion
from utils.main_process import main_process


@retry(
    stop=stop_after_attempt(30),
    retry=retry_if_exception_type(RetryExceprion)
)
def get_archives(job_id: int) -> tuple[bytes]:
    """Получение архивов с изображениями и аннотациями"""
    
    image_archive_response = session.get(
        url=f"{settings.API_URL}/jobs/{job_id}/data",
        params={
            "type": "chunk",
            "number": 0,
        },
    )
    
    annotations_archive_response = session.get(
        url=f"{settings.API_URL}/jobs/{job_id}/annotations",
        params={
            "action": "download",
            "format": r"CVAT%20for%20images%201.1",
        },
    )
    
    if not image_archive_response.content or not annotations_archive_response.content:
        raise RetryExceprion
    
    return image_archive_response.content, annotations_archive_response.content


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
