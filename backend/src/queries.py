from tenacity import retry
from tenacity import stop_after_attempt

from backend.src.session import session
from backend.src.settings import settings


@retry(stop=stop_after_attempt(10000))
def get_jobs_data(_id: int, _format: str) -> tuple[bytes]:
    """
    Get tuple with 2 archives: images and annotations.
    """
    archive = session.get(
        f"{settings.API_URL}/jobs/{_id}/data?type=chunk&number=0",
    ).content

    annotations = session.get(
        f"{settings.API_URL}/jobs/{_id}/annotations?action=download&format={_format}",
    ).content

    if not archive or not annotations:
        raise Exception

    return archive, annotations


@retry(stop=stop_after_attempt(10000))
def get_jobs_list(task_id: int) -> list[int]:
    """
    Get list of jobs from task.
    """
    print(f"Trying to get jobs list from task #{task_id}...\n")
    jobs = []
    try:
        response = session.get(
            f"{settings.API_URL}/jobs?task_id={task_id}&page_size={1e10}"
        ).json()
        for job in response["results"]:
            jobs.append(int(job["id"]))
        print(f"Seccessfuly getting the jobs list from task #{task_id}")
    except Exception as e:
        print(f"ERROR: {repr(e)}: getting jobs id from task #{task_id}")
    return jobs
