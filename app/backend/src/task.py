from typing import final
import shutil
import os
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt

from app.backend.src.exceptions import RetryExceprion
from app.backend.src.exceptions import TaskNotFoundError
from app.backend.src.exceptions import NotAuthorizedError
from app.backend.src.session import session
from app.backend.src.settings import settings


@final
class Task:
    """Класс сущности task"""

    def __init__(self, task_id: int):
        self.task_id = task_id
        self.jobs_id = self.get_jobs_id()

    @retry(
        stop=stop_after_attempt(30),
        retry=retry_if_exception_type(RetryExceprion),
    )
    def get_jobs_id(self) -> list:
        """
        Получить список из id всех job, которые есть в таске.

        :return: Список id job.
        """
        jobs_id_list = list()
        response = session.get(
            url=f"{settings.API_URL}/jobs",
            params={
                "task_id": self.task_id,
                "page": 1,
                "page_size": int(1e10),
            },
        )
        if response.status_code == 401:
            raise NotAuthorizedError()
        result = response.json()
        if not result:
            RetryExceprion()
        if response.status_code == 400:
            raise TaskNotFoundError()
        for job in result["results"]:
            jobs_id_list.append(int(job["id"]))
        return jobs_id_list

    def create_path(self):
        """Создание директории для task"""

        self.path = settings.RESULT_PATH / str(self.task_id)
        if self.path.exists():
            shutil.rmtree(self.path)
        os.mkdir(self.path)
