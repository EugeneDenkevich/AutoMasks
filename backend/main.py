from typing import Literal, Optional
from pathlib import Path

from backend.src.instance import process_instance
from backend.src.queries import get_jobs_list
from backend.src.session import session
from backend.src.settings import settings
from utils.main_process import main_process
from utils.main_process import process_end

from backend.src.converters import row_data_to_dto
from backend.src.schemas import InputDTO
from backend.src.enums import TypeEnum
from backend.src.handlers import handle_job
from backend.src.handlers import handle_task
from backend.src.handlers import handle_project


def main_(
    username: Optional[str] = None,
    password: Optional[str] = None,
    id_list: Optional[str] = None,
    type: Optional[str] = None,
    transparency: Optional[str] = None,
) -> None:
    """Главная функция бэкенда"""

    # Переводим сырые данные в модель DTO.
    input: InputDTO = row_data_to_dto(
        username=username,
        password=password,
        id_list=id_list,
        type=type,
        transparency=transparency,
    )

    # Входим в систему CVAT.
    session.auth = (input.username, input.username)
    
    # Устанавливаем прозрачность.
    settings.TRANSPARENCY = input.transparency

    # Обрабатываем данные по типу сущности.
    if input.type == TypeEnum.JOBS:
        for job_id in input.id_list:
            handle_job(job_id)
    if input.type == TypeEnum.TASKS:
        for task_id in input.id_list:
            handle_task(task_id)
    if input.type == TypeEnum.PROJECTS:
        for project_id in input.id_list:
            handle_project(project_id)







class ResultPath(str):
    pass













def main(
    id_list: list[int],
    _type: Literal["jobs", "tasks"] = "jobs",
    _format: str = "CVAT for images 1.1",
    transparency: int = 100,
    type_element: Literal["polygon", "box"] = "polygon",
    login: str = "",
    password: str = "",
) -> ResultPath:
    """
    Main function.\n
    Get
    - _type: type of the instances (jobs or tasks);
    - id_list: list of tasks or jobs id;
    - transparency: mask's transparency, in %.\n
    Return
    - ResultPath: path to result directory with porcessed images.
    """
    if not login or not password:
        pass
    if not settings.RESULT_PATH.exists():
        settings.RESULT_PATH.mkdir()

    session.auth = (login, password)
    _format = _format.replace(" ", "%20")

    jobs_list = []
    if _type == "tasks":
        for task_id in id_list:
            jobs_list.extend(get_jobs_list(task_id))
    elif _type == "jobs":
        jobs_list = id_list
    elif _type == "projects":
        raise NotImplemented
    else:
        raise ValueError("Incorrect type of processed instance.")

    for _id in jobs_list:
        if not main_process.over:
            process_instance(
                _id,
                _format,
                transparency,
            )
        else:
            process_end()
            return
    result_path = ResultPath(settings.RESULT_PATH)

    return result_path
