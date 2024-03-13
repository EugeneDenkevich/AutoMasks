import os

from app.frontend.exceptions import CantOpenFileError


def open_depends_os(path: str) -> None:
    try:
        os.startfile(path)  # Для Windows
    except:
        try:
            os.system(f"open {path}")  # Для macOS
        except:
            try:
                os.system(f"xdg-open {path}")  # Для Linux
            except:
                raise CantOpenFileError()
