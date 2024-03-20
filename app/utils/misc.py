import os
import logging
from pathlib import Path
import platform
import sys
import subprocess

from app.frontend.exceptions import CantOpenFileError


def open_depends_os(path: str) -> None:
    path = str(get_result_path())
    os_name = platform.system()
    if os_name.lower() == "windows":
        os.startfile(path)
    if os_name.lower() == "darwin":
        os.system(f"open {path}")
    if os_name.lower() == "linux":
        os.system(f"xdg-open {path}")
    else:
        logging.error(f"Ошибка открытия директории: OS: {os_name}, PATH: {path}")
        raise CantOpenFileError()


def get_result_path() -> Path:
    """
    Создаёт папку 'result' и возвращает путь к ней.
    Существует, потому что существует macos.

    :return: Путь к папке 'result'
    """
    created = False
    os_name = platform.system()
    # TODO Сделать везде home вне зависимости от ОС
    if os_name == "Darwin":
        result_path = Path.home() / ".automask" / "result"
        if not result_path.exists():
            os.makedirs(result_path)
            created = True
        # os.system(f'mkdir -p {result_path}')
    else:
        result_path = Path(sys.argv[0]).parent.resolve() / "result"
        if not result_path.exists():
            os.makedirs(result_path)
            created = True
    if created:
        logging.info(f"Директория 'result' была создана: {result_path}")
    return result_path
