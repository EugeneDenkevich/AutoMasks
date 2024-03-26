import os
import logging
from pathlib import Path
import platform

from app.frontend.exceptions import CantOpenFileError


def open_depends_os(path: str) -> None:
    path = str(get_result_path())
    os_name = platform.system()
    if os_name.lower() == "windows":
        os.startfile(path)
    elif os_name.lower() == "darwin":
        os.system(f"open {path}")
    elif os_name.lower() == "linux":
        os.system(f"xdg-open {path}")
    else:
        logging.error(f"Ошибка открытия директории: OS: {os_name}, PATH: {path}")
        raise CantOpenFileError()


def get_result_path() -> Path:
    """
    Возвращает путь к папке 'result'.
    Если её нет - создаёт её в домашней директории пользователя.

    :return: Путь к папке 'result'.
    """
    result_path = Path.home() / ".automask" / "result"
    if not result_path.exists():
        os.makedirs(result_path)
        logging.info(f"Директория 'result' была создана: {result_path}")
    return result_path


def get_db_path() -> str:
    """
    Возвращает путь к файлу sqlite базщы данных.

    :return: Путь к файлу sqlite базщы данных.
    """
    db_path = Path.home() / ".automask" / "mask.db"
    return db_path
