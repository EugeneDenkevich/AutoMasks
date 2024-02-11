from dataclasses import dataclass
from typing import final


@final
@dataclass
class MainProcess:
    over: bool = False

    def cancel(self):
        """
        Finish the processing on backend.
        """
        pass

main_process = MainProcess()


def process_end():
    """
    Finish the process of image processing on backend.
    """
    pass
