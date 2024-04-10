from typing import Optional
from httpx import BasicAuth

from app.backend.src.converters import row_data_to_dto
from app.backend.src.enums import TypeEnum
from app.backend.src.handlers import handle_job
from app.backend.src.handlers import handle_project
from app.backend.src.handlers import handle_task
from app.backend.src.schemas import InputDTO
from app.backend.src.session import session
from app.backend.src.settings import settings
from app.backend.src.gateways.db import db_sqlite


def main(
    username: Optional[str] = None,
    password: Optional[str] = None,
    id_list: Optional[str] = None,
    type: Optional[str] = None,
    transparency: Optional[str] = None,
    **kwargs,
) -> None:
    """Главная функция бэкенда"""

    # Переводим введённые данные в модель DTO:
    input: InputDTO = row_data_to_dto(
        username=username,
        password=password,
        id_list=id_list,
        type=type,
        transparency=transparency,
    )

    # Устанавливаем прозрачность:
    settings.TRANSPARENCY = input.transparency

    # Входим в систему CVAT.
    session.auth = (
        BasicAuth(
            username=input.username,
            password=input.password,
        )
    )
    db_sqlite.save_credentials(
        input.username,
        input.password,
    )

    # Обрабатываем данные по типу сущности.
    if input.type == TypeEnum.JOBS:
        for id_job in input.id_list:
            handle_job(id_job, **kwargs)
    if input.type == TypeEnum.TASKS:
        for id_task in input.id_list:
            handle_task(id_task, **kwargs)
    if input.type == TypeEnum.PROJECTS:
        for id_project in input.id_list:
            handle_project(id_project, **kwargs)
