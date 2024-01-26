from typing import Literal

from src.instance import process_instance
from src.settings import settings


class ResultPath(str):
    pass


def main(
    id_list: list[int],
    _type: Literal["jobs", "tasks"] = "jobs",
    _format: str = "CVAT for images 1.1",
    transparency: int = 100,
    type_element: Literal["polygon", "box"] = "polygon",
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
    if not settings.RESULT_PATH.exists():
        settings.RESULT_PATH.mkdir()

    _format = _format.replace(" ", "%20")
    for _id in id_list:
        process_instance(_id, _type, _format, transparency, type_element)

    result_path = ResultPath(settings.RESULT_PATH)

    return result_path


"""
Фиксми:
1. Ругается, если в папке result уже есть такие же файлы. Найти где это происходит и сделать перезаписывание этих файлов.
2. Сделать имена итоговых изображений так, как они называются в папке.
3. Сейчас требуется введение либо полигонов, либо боксов: сделать авто-определение.
"""
