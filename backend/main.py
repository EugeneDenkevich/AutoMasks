from typing import Literal

from backend.src.instance import process_instance
from backend.src.session import session
from backend.src.settings import settings
from utils.main_process import main_process
from utils.main_process import process_end


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
        # fixme #4
        pass
    if not settings.RESULT_PATH.exists():
        settings.RESULT_PATH.mkdir()

    session.auth = (login, password)
    _format = _format.replace(" ", "%20")
    for _id in id_list:
        if not main_process.over:
            process_instance(
                _id,
                _type,
                _format,
                transparency,
                type_element,
            )
        else:
            process_end()
            return
    result_path = ResultPath(settings.RESULT_PATH)

    return result_path


# fixme #5
# Сделать имена итоговых изображений так, как они называются в папке.

# fixme #6
# Сейчас требуется введение либо полигонов, либо боксов: сделать авто-определение.
