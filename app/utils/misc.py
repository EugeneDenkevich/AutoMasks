import os
import logging
from pathlib import Path
import platform
import sys

from app.frontend.exceptions import CantOpenFileError


def open_depends_os(path: str) -> None:
    os_name = platform.system()
    if os_name.lower() == "windows":
        os.startfile(path)
    if os_name.lower() in ["darwin", "posix"]:
        os.system(f"open {path}")
    if os_name.lower() == "linux":
        os.system(f"xdg-open {path}")
    else:
        logging.error(f"Ошибка открытия директории: OS: {os.name}, PATH: {path}")
        raise CantOpenFileError()


def create_result_path() -> str:
    """
    Создаёт папку 'result' и возвращает путь к ней.
    Существует, потому что существует macos.

    :return: Путь к папке 'result'
    """
    os_name = platform.system()
    if os_name == "Darwin":
        # result_path = "~/.automask/result/"
        result_path = Path("~/.automask/result/")
    else:
        result_path = Path(sys.argv[0]).parent.resolve() / "result"
    if not Path(result_path).exists():
        os.makedirs(result_path)
    logging.info(f"Директория 'result' была создана: {result_path}")
    return str(result_path)
