import os
import platform

from app.frontend.exceptions import CantOpenFileError


def open_depends_os(path: str) -> None:
    os_name = platform.system()
    if os_name == "Windows":
        os.startfile(path)
    if os_name == "Darwin":
        os.system(f"open {path}")
    if os_name == "Linux":
        os.system(f"xdg-open {path}")
    else:
        raise CantOpenFileError()
